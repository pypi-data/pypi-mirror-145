from lyberry_api import pub
from lyberry_api.claim import LBRY_Claim

class LBRY_Channel(LBRY_Claim):
    def __init__(self, claim, LBRY_api):
        super(LBRY_Channel, self).__init__(claim, LBRY_api)

        if claim["value_type"] != "channel":
            raise ValueError('This not a channel')
        
        if self.is_repost:
            self.reposter = pub.get_channel_from_claim(self.reposted_raw, LBRY_api)

        try:
            self.thumbnail = claim['value']['thumbnail']['url']
        except KeyError:
            self.thumbnail = ''

        self.title = claim['value']['title'] if 'title' in claim['value'] else self.name
        self.pubs_feed = self.get_pubs_feed()

    def __str__(self):
        return f"LBRY_Channel({self.name})"
    
    def get_pubs_feed(self):
        return self._LBRY_api.channels_feed([self.id])

    def refresh_feed(self):
        self.pubs_feed = self.get_pubs_feed()

    def follow(self):
        self._LBRY_api.add_sub_url(self.raw['permanent_url'])

    def unfollow(self):
        self._LBRY_api.remove_sub_url(self.raw['permanent_url'])

    @property
    def is_followed(self):
        return self.raw['permanent_url'] in self._LBRY_api.subs_urls

    def search(self, text: str):
        return self._LBRY_api.claim_search_results({
            "text": text,
            "channel": self.url,
            })

class LBRY_Channel_Err(LBRY_Channel):
    def __init__(self):
        self.name = 'Error'
        self.id = '0'
        self.url = ''
        self.title = ''
        self.description = ''
        self.pubs = []
        self.pubs_feed = iter([])

    def __str__(self):
        return f"Errored LBRY_Channel({self.name})"
    
    def get_pubs_feed(self):
        return iter([])

