
from .generic import Generic
import re
from listen import log


class Kpop(Generic):

    def get_track(self, unformatted_string):
        # Get rid of non-ascii and stuff between [] (usually genre)
        clean_string = re.sub(r'[^\x00-\x7F]+', ' ', unformatted_string)
        clean_string = re.sub(r'\[[^)]*\]', '', clean_string)
        # Sometime they put the english title in brackets - grab it for now
        backup_title_regex = r'^.*-.*?\(([\w\ ]*)\)'
        backup_title = re.search(backup_title_regex, clean_string)
        clean_string = re.sub(r'\([^)]*\)', '', clean_string)
        # Basic artist - title should be ok
        artist_regex = r'^(.*?)\s*-'
        title_regex = r'-\s*(.*)'
        artist = re.search(artist_regex, clean_string)
        if artist:
            artist_string = artist.group(1)
            title = re.search(title_regex, clean_string)
            if title:
                title_string = title.group(1)
                if len(title_string) > 1:
                    return '%s %s' % (artist_string, title_string)
            if backup_title:
                title_string = backup_title.group(1)
                if len(title_string) > 1:
                    return '%s %s' %(artist_string, title_string)
        log.warning(unformatted_string)
        return None
