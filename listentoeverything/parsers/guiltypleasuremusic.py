
from .generic import Generic
import re
from listen import log


class Guiltypleasuremusic(Generic):

    def get_playlist(self):
        playlists = {}

        playlist_name = 'r/%s - Hot' % self.subreddit_name
        playlists[playlist_name] = []
        for post in self.reddit.subreddit(self.subreddit_name).hot(limit=200):
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

        playlist_name = 'r/%s - Top all time' % self.subreddit_name
        playlists[playlist_name] = []
        for post in self.reddit.subreddit(self.subreddit_name).top('all'):
            track_title = self.get_track(post.title)
            if track_title:
                playlists[playlist_name].append(track_title)
        playlists[playlist_name] = playlists[playlist_name][:50]

        return playlists