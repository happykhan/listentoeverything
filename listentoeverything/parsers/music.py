from .generic import Generic
import re
from listen import log


class Music(Generic):

    def get_track(self, unformatted_string):
        regex = r'(.*) - (.*?)\s*(\(.*\)*|)\['
        track = re.search(regex, unformatted_string)
        if track:
            return '%s %s' % (track.group(1), track.group(2))
        log.warning(unformatted_string)
        return None

