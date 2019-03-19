import re
import praw
from listen import log


class Generic:

    def __init__(self, subreddit_name, cfg, limit_no=50):
        self.cfg = cfg
        self.subreddit_name = subreddit_name
        self.reddit = self.get_reddit_session(self.cfg)
        self.subscribers = self.reddit.subreddit(subreddit_name).subscribers
        self.limit_no=limit_no


    def get_reddit_session(self, cfg):
        reddit = praw.Reddit(
            client_id=cfg["reddit"]["client_id"],
            client_secret=cfg["reddit"]["client_secret"],
            user_agent=cfg["reddit"]["user_agent"],
            username=cfg["reddit"]["username"],
            password=cfg["reddit"]["password"],
        )
        return reddit

    def get_track(self, unformatted_string):
        clean1_string = re.sub(r'\([^)]*\)', '', unformatted_string)
        clean2_string = re.sub(r'\[[^)]*\]', '', clean1_string)
        regex = r'(.*)\s*-\s*([\w\s\'\-\.]+)\s*$'
        reg = re.search(regex, clean2_string)
        if reg:
            return "%s %s" % (reg.group(1), reg.group(2))
        else:
            log.warning(clean2_string)
            return None

    def get_playlist(self):
        playlists = {}
        if self.subscribers > 20000:
            log.info('Subscribers over %d, creating hot list' % self.subscribers)
            playlist_name = 'r/%s - Hot' % self.subreddit_name
            playlists[playlist_name] = []
            for post in self.reddit.subreddit(self.subreddit_name).hot(limit=100):
                track_title = self.get_track(post.title)
                if track_title:
                    playlists[playlist_name].append(track_title)
            playlists[playlist_name] = playlists[playlist_name][:50]
        playlist_name = 'r/%s - Top this week' % self.subreddit_name
        playlists[playlist_name] = []
        for post in self.reddit.subreddit(self.subreddit_name).top('week'):
            track_title = self.get_track(post.title)
            if track_title:
                playlists[playlist_name].append(track_title)
        playlists[playlist_name] = playlists[playlist_name][:50]
        return playlists

    def get_test_data(self, get_limit=300):
        return [x.title for x in self.reddit.subreddit(self.subreddit_name).hot(limit=get_limit)]
