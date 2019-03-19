from .generic import Generic
import re
from listen import log


class Listentothis(Generic):

    def get_track(self, unformatted_string):
        regex = r'(.*?)\s*[-—]+\s*(.*?)\s*(\(.*\)*|)\['
        track = re.search(regex, unformatted_string)
        if track:
            return '%s %s' % (track.group(1).strip(), track.group(2).strip())
        log.warning(unformatted_string)
        return None

