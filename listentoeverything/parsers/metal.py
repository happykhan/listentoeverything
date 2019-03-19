from .generic import Generic
import re
from listen import log


class Metal(Generic):

    def get_track(self, unformatted_string):
        clean1_string = re.sub(r'\([^)]*\)', '', unformatted_string)
        clean2_string = re.sub(r'\[[^)]*\]', '', clean1_string)
        regex = r'(.*)\s*-\s*([\w\s\'\-\.]+)\s*$'
        track = re.search(regex, clean2_string)
        if track:
            return '%s %s' % (track.group(1).strip(), track.group(2).strip())
        log.warning(unformatted_string)
        return None
