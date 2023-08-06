import re

import lyberry_api.channel
from lyberry_api.claim import LBRY_Claim
import lyberry_api.settings

def get_channel_from_claim(claim, LBRY_api):
    if "signing_channel" in claim:
        channel_claim = claim['signing_channel']
        try:
            return lyberry_api.channel.LBRY_Channel(channel_claim, LBRY_api)
        except ValueError:
            return lyberry_api.channel.LBRY_Channel_Err(LBRY_api)
    else:
        return lyberry_api.channel.LBRY_Channel_Err(LBRY_api)

class LBRY_Pub(LBRY_Claim):
    def __init__(self, claim, LBRY_api, channel = {}):
        super(LBRY_Pub, self).__init__(claim, LBRY_api)

        if self.raw["value_type"] == "channel":
            raise ValueError('This is a channel, not a publication')
        
        if self.is_repost:
            self.reposter = get_channel_from_claim(self.reposted_raw, LBRY_api)

        self.channel = get_channel_from_claim(claim, LBRY_api)
        self.title = self.raw['value']['title']
        self.media_type = claim['value']['source']['media_type'] if 'source' in claim['value'] else 'video'
        self.license = claim['value']['license'] if 'license' in claim['value'] else 'Undefined'

    def __str__(self):
        return f"LBRY_Pub({self.title})"

    def get_content(self):
        self.raw = self._LBRY_api.get(self.url)
        return self.raw

    @property
    def streaming_url(self):
        self.get_content()
        return self.raw['streaming_url']

    @property
    def download_path(self):
        self.get_content()
        return self.raw['download_path']

    def open_external(self):
        self.make_chapter_file()
        file_type = self.media_type.split("/")[0]
        if file_type == "video" or file_type == "audio":
            lyberry_api.settings.media_player(self.streaming_url, self.download_path, self.title)
        elif file_type == "text":
            lyberry_api.settings.text_viewer(self.streaming_url, self.download_path, self.title)

    def make_chapter_file(self):
        with open('/tmp/lyberry_chapters', 'w') as chapters_file:
            chapters_file.write(self.desc_to_ffmetadata(self.description))

    def desc_to_ffmetadata(self, desc: str, end: int = 0) -> str:
        lines = desc.split('\n')
        matches = []
        for line in lines:
            match = re.match(r'\s*(\d+:\d+(:\d+)?)\s(.*)', line)
            if match:
                matches.append(match)

        stamps = []
        for match in matches:
            raw_time = match.group(1)
            times = raw_time.split(':')
            if len(times) == 2:
                [minutes, seconds] = times
                hours = 0
            elif len(times) == 3:
                [hours, minutes, seconds] = times
            time = int(hours)*3600 + int(minutes)*60 + int(seconds)
            title = match.group(3)
            stamps.append([time, title])

        out = ';FFMETADATA1'
        for i, stamp in enumerate(stamps):
            time = stamp[0]
            title = stamp[1]
            out += f'''
[CHAPTER]
TIMEBASE=1/1
START={time}
    '''
            if i+1 < len(stamps):
                next_time = stamps[i+1][0]
                out += f'END={next_time}\n'
            elif end != 0:
                out += f'END={end}\n'
            else:
                out += f'END={next_time + 100}\n'
            out += f'title={title}\n'
        return out

