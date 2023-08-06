from lyberry_api.comment import LBRY_Comment

class LBRY_Claim():
    def __init__(self, claim, LBRY_api):
        self._LBRY_api = LBRY_api
        if claim["value_type"] == "repost":
            self.is_repost = True
            self.reposted_raw = claim
            claim = claim["reposted_claim"]
        else:
            self.is_repost = False
        self.raw = claim
        self.id = claim['claim_id']
        self.timestamp = claim['timestamp']
        self.name = claim['name']
        # some claims don't have a canonical or short url, eg channel_list
        self.url = claim['canonical_url'] if 'canonical_url' in claim else claim['permanent_url']
        self.short_url = claim['short_url'] if 'short_url' in claim else claim['permanent_url']
        self.permanent_url = claim['permanent_url']
        self.description = claim['value']['description'] if 'description' in claim['value'] else 'No Description'
        try:
            self.thumbnail = claim['value']['thumbnail']['url']
        except KeyError:
            self.thumbnail = ''
        self.comments_feed = self.get_comments_feed()

    def __str__(self):
        return f"LBRY_Pub({self.title})"

    def set_reposter(self, reposter):
        self.is_repost = True
        self.reposter = reposter

    def refresh_comments_feed(self):
        self.comments_feed = self.get_comments_feed()

    def get_comments_feed(self):
        page = 1
        self._comments = []
        while True:
            raw_comments = self._LBRY_api.list_comments(self, page=page)
            if not 'items' in raw_comments:
                break
            new_comments = []
            for raw_comment in raw_comments["items"]:
                new_comments.append(LBRY_Comment(raw_comment, self._LBRY_api, self))
            self._comments.extend(new_comments)
            for comment in new_comments:
                yield comment
            page += 1

    def create_comment(self, commenter, msg):
        self._LBRY_api.make_comment(commenter, msg, self)

    def repost(self, bid: float, channel, preview: bool = False):
        return self._LBRY_api.request('stream_repost', {
            "name": self.name,
            "claim_id": self.id,
            "bid": str(bid),
            "channel_id": channel.id,
            "preview": preview})
