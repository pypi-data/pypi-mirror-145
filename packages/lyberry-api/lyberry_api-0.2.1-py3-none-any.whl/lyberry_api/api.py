import requests
import time
import json
import re
import lyberry_api.channel
import lyberry_api.pub
import lyberry_api.account
from lyberry_api.settings import settings

class LBRY_Api():
    ONLINE = 0
    OFFLINE = 1
    INITIALISING = 2
    def __init__(self,
            comment_api = settings['comment_api'] or 'https://comments.odysee.com/api/v2',
            lbrynet_api = settings['lbrynet_api'] or 'http://localhost:5279',
            lighthouse_api = settings['lighthouse_api'] or "https://lighthouse.odysee.tv",
            wallet_id = 'default_wallet',
            ):
        self.comment_api = comment_api
        self.lbrynet_api = lbrynet_api
        self.lighthouse_api = lighthouse_api
        wallet_id = wallet_id or settings['default_wallet']
        self.wallet_id = wallet_id

    def connect(self, dur = 10):
        print('connecting to lbrynet')
        attempts = 0
        while attempts < dur:
            try:
                status = self.status
            except ConnectionError:
                yield 1
                attempts += 1
                time.sleep(1)
                continue
            if status['is_running'] if 'is_running' in status else False:
                yield 0
            yield 2
            time.sleep(1)
        raise ConnectionError('Could not connect to lbrynet')

    def initialising(self):
        try:
            status = self.status
        except ConnectionError:
            return False
        if status['is_running'] if 'is_running' in status else False:
            return False
        return True

    def online(self):
        try:
            status = self.status
            return status[ 'is_running' ]
        except:
            return False

    def apply_settings(self):
        from lyberry_api.settings import settings as new_settings
        self.lbrynet_api = new_settings['lbrynet_api']
        self.comment_api = new_settings['comment_api']
        self.lighthouse_api = new_settings['lighthouse_api']
        self.wallet_id = new_settings['default_wallet']

    @property
    def status(self):
        return self.exact_request('status', timeout = 1)

    @property
    def components_status(self):
        return self.status["startup_status"]

    def request(self, method, params = {}):
        params.update({'wallet_id': self.wallet_id})
        try:
            return self.exact_request(method, params)
        except ValueError as err:
            if err.args[0]['message'].startswith("Couldn't find wallet"):
                self.create_wallet(self.wallet_id)
                return self.request(method, params)
            else:
                raise err

    def exact_request(self, method, params = {}, timeout = 10):
        try:
            res = requests.post(self.lbrynet_api, json={"method": method, "params": params}, timeout = timeout)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('cannot reach lbrynet')
        if not res.ok:
            raise ConnectionError(res.text)
        res_data = res.json()
        if 'error' in res_data:
            raise ValueError(res_data["error"])
        if not 'result' in res_data:
            raise ValueError(f'lbrynet returned no result: {res_data}')
        return res_data['result']

    def id_from_url(self, lbry_url):
        match = re.match(r'lbry://@.*?[:#]([a-f0-9]*)$', lbry_url);
        if match == None:
            raise ValueError(f'could not find id in lbry url: {lbry_url}')
        return match.group(1)

    def get(self, uri):
        if type(uri) != str:
            raise TypeError('Tried to get a URI that was not a string')
        return self.request('get', {'uri': uri})

    def resolve_raw(self, uri):
        res = self.request('resolve', {'urls': uri})[uri]
        if 'error' in res:
            error = res['error']
            raise ValueError(f"lbrynet returned an error:\n{error}")
        return res

    @property
    def subs_urls(self):
        prefs = self.get_shared_prefs()
        if not 'value' in prefs or not 'subscriptions' in prefs['value']:
            self.init_pref()
            prefs = self.get_shared_prefs()
        val = prefs['value']['subscriptions']
        return val

    def add_sub_url(self, url):
        url_id = self.id_from_url(url)
        subs_urls = self.subs_urls
        if not url in subs_urls:
            subs_urls.append(url)
            self.set_subs(subs_urls)

    def remove_sub_url(self, url):
        subs_urls = self.subs_urls
        if url in subs_urls:
            subs_urls.remove(url)
            self.set_subs(subs_urls)

    def set_subs(self, subs_list):
        self.set_pref('shared', {'value': {'subscriptions': subs_list}})

    def get_shared_prefs(self):
        prefs_raw = self.prefs
        if not 'shared' in prefs_raw:
            self.init_pref()
            prefs_raw = self.prefs
        return prefs_raw['shared']

    @property
    def prefs(self):
        return self.request('preference_get')

    def init_pref(self):
        self.set_subs([])

    def set_pref(self, key, value):
        self.request('preference_set', {'key':key, 'value':value})

    @property
    def subs_ids(self):
        return [self.id_from_url(url) for url in self.subs_urls]

    @property
    def sub_feed(self, page_size = 20):
        return self.channels_feed(self.subs_ids, page_size)

    def list_comments(self, claim, parent = None, page = 1, page_size = 20, sort_by = 3):
        params = {
            "claim_id": claim.id,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "top_level": True,
        }
        if parent:
            params["parent_id"] = parent.id
            params["top_level"] = False

        res = requests.post(
            self.comment_api,
            json={
                "method": "comment.List",
                "id": 1,
                "jsonrpc":"2.0",
                "params": params
            }
        ).json()
        return res['result']

    def sign(self, channel, string):
        data = string.encode('utf-8')
        return self.request("channel_sign", {
            "channel_name": channel.name, 
            "hexdata": data.hex(),
            })

    def make_comment(self, commenter, comment, claim, parent = None):
        params = {
            "channel_id": commenter.id,
            "channel_name": commenter.name,
            "claim_id": claim.id,
            "comment": comment,
        }
        params.update(self.sign(commenter, comment))

        if parent:
            params["parent_id"] = parent.id

        try:
            res = requests.post(self.comment_api, json={"method": "comment.Create", "id": 1, "jsonrpc":"2.0", "params": params}).json()
            return res['result']
        except:
            raise Exception(res)

    def channel_from_uri(self, uri):
        raw_claim = self.resolve_raw(uri)
        if 'error' in raw_claim:
            error = raw_claim['error']
            print(f"lbrynet returned an error:\n{error['name']}: {error['text']}")
            return lyberry_api.channel.LBRY_Channel_Err()
        else:
            channel = lyberry_api.channel.LBRY_Channel(raw_claim, self)
            return channel

    def pub_from_uri(self, uri):
        raw_claim = self.resolve_raw(uri)
        return lyberry_api.pub.LBRY_Pub(raw_claim, self)

    def resolve(self, uri):
        raw_claim = self.resolve_raw(uri)
        if 'error' in raw_claim:
            error = raw_claim['error']
            raise Exception(f"lbrynet returned an error:\n{error['name']}: {error['text']}")
        return self.claim_to_object(raw_claim)

    def claim_to_object(self, claim):
        if not 'value_type' in claim:
            raise ValueError('Malformed claim, no value type')
        value_type = claim['value_type']
        if value_type == 'repost':
            if 'reposted_claim' in claim:
                obj = self.claim_to_object(claim['reposted_claim'])
                channel = lyberry_api.pub.get_channel_from_claim(claim, self)
                obj.set_reposter(channel)
                return obj
            else:
                raise ValueError('Malformed claim, repost but no reposted claim')
        elif value_type == 'channel':
            return lyberry_api.channel.LBRY_Channel(claim, self)
        elif value_type == 'stream':
            return lyberry_api.pub.LBRY_Pub(claim, self)
        else:
            raise ValueError(f'Unsupported claim type {claim["value_type"]}')

    @property
    def my_channels(self):
        raw_channels = self.request("channel_list")["items"]
        channels = []
        for raw_channel in raw_channels:
            channel = lyberry_api.channel.LBRY_Channel(raw_channel, self)
            channels.append(channel)
        return list(channels)

    def add_account(self, name, priv_key):
        raw_account = self.request('account_add', {
            "account_name": name,
            "private_key": priv_key,})

        return lyberry_api.account.LBRY_Account(raw_account, self, self.wallet_id)

    def remove_account(self, account_id):
        self.request('account_remove', {
            'account_id': account_id.id,})

    @property
    def accounts(self):
        raw_account_list = self.request('account_list')['items']
        account_list = [
                lyberry_api.account.LBRY_Account(account_raw, self, self.wallet_id) for account_raw in raw_account_list]
        return account_list

    def set_default_account(self, account_id):
        self.request('account_set', {
            'account_id': account_id,
            'default': True,})

    @property
    def default_account(self):
        accounts = self.accounts
        for account in accounts:
            if account.is_default:
                return account
        raise Exception('No default account')

    def claim_search_results(self, params, page_size = 20):
        page = 1
        while True:
            latest_raw = self.claim_search_raw(params, page, page_size)
            if len(latest_raw['items']) == 0:
                break
            for item in latest_raw['items']:
                try:
                    yield self.claim_to_object(item)
                except Exception as err:
                    print(err)
                    continue
            page += 1

    def claim_search_raw(self, params, page = 1, page_size = 20):
        return self.request('claim_search', {
            "page": page,
            "page_size": page_size,
            "not_tags": ["nsfw"],
            **params
        })

    def lbrynet_search_feed(self, name: str = "", text: str = "", page_size: int = 20, params: dict = {}):
        if name and not text:
            return self.claim_search_results({"name": name}, page_size)
        elif text and not name:
            return self.claim_search_results({"text": text}, page_size)

        else:
            return ValueError("Must give either name or text")

    def lighthouse_search_raw(self, query: str, page: int = 1, page_size: int = 20, claimType: str = "file"):
        start = (page - 1) * page_size
        url = f"{self.lighthouse_api}/search?s={query}&from={start}&size={page_size}&claimType={claimType}"
        return requests.get(url).json()

    def lighthouse_search_results(self, query: str, page_size: int = 20):
        page = 1
        while True:
            latest_raw = self.lighthouse_search_raw(query, page, page_size)
            if len(latest_raw) == 0:
                break
            for item in latest_raw:
                claim_id = item["claimId"]
                name = item["name"]
                uri = f"lbry://{name}#{claim_id}"
                yield self.resolve(uri)
            page += 1

    def lighthouse_search_feed(self, query: str, page_size: int = 20):
        return self.lighthouse_search_results(query, page_size)

    def channels_feed(self, ids: list, page_size=20):
        return self.claim_search_results({"order_by": "release_time", "channel_ids": ids}, page_size)

    def create_wallet(self, name: str, create_account: bool = True):
        self.request('wallet_create', {'wallet_id': name, 'create_account': create_account})

    @property
    def balance(self):
        return self.request('wallet_balance', {'wallet_id': self.wallet_id})

    @property
    def wallets(self):
        return self.exact_request('wallet_list')['items']

