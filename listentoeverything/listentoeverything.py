# -*- coding: utf-8 -*-

"""Main module."""
import praw
import logging
import spotipy
import yaml
from spotipy.util import prompt_for_user_token
from os import path
import re
import datetime

logging.basicConfig()
log = logging.getLogger()


def load_config(config_file=path.join(path.expanduser("~"), ".listen.yml")):
    with open(config_file, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return cfg
    log.warning('No config found')
    return None


def get_reddit_session(cfg):
    reddit = praw.Reddit(
        client_id=cfg["reddit"]["client_id"],
        client_secret=cfg["reddit"]["client_secret"],
        user_agent=cfg["reddit"]["user_agent"],
        username=cfg["reddit"]["username"],
        password=cfg["reddit"]["password"],
    )
    return reddit


def get_spotify_session(cfg):
    token = prompt_for_user_token(
        cfg["spotify"]["username"],
        cfg["spotify"]["scope"],
        client_id=cfg["spotify"]["client_id"],
        client_secret=cfg["spotify"]["client_secret"],
        redirect_uri=cfg["spotify"]["redirect_uri"],
    )
    spotify = spotipy.Spotify(auth=token)
    return spotify


def get_current_playlist_name(subreddit):
    today = datetime.date.today()
    monday_date = today - datetime.timedelta(days=today.weekday())
    return 'r-listento%s %s' % (subreddit.replace('listento', ''), str(monday_date))


def update_playlist(cfg, spotify, reddit, subreddit_name):
    user = cfg["spotify"]["username"]
    playlist_name = get_current_playlist_name(subreddit_name)
    # Find existing playlist or create a new one
    playlist = [
        x.get("id")
        for x in spotify.current_user_playlists().get("items")
        if x.get("name") == playlist_name
    ]
    if playlist:
        playlist = playlist[0]
    else:
        playlist = spotify.user_playlist_create(user, playlist_name)
        playlist = playlist.get('id')

    # Find existing tracks, save the URI
    existing_tracks = spotify.user_playlist_tracks(user, playlist)
    if existing_tracks:
        existing_tracks = [
            x.get("track").get("uri") for x in existing_tracks.get("items")
        ]
    else:
        existing_tracks = []
    new_tracks = []
    regex = (
        r"^([\w\s\(\)\'\&\,\!\.]+?)\s*-\s*([\w\s\'\&\,\!\/\’\.\(\)]+?)(\s*\[.+\]|$)"
    )  # Ridiculous regex looking for artist - title
    not_found = []
    # Search reddit for artist - titles, add to spotify playlist list if its not in the playlist already
    for x in reddit.subreddit(subreddit_name).top("week"):
        reg = re.search(regex, x.title.replace("--", "-"))
        if reg:
            track_name = "%s - %s" % (reg.group(1), reg.group(2))
            log.debug("Looking for %s as %s" % (x.title, track_name))
            track = spotify.search(track_name, type="track", limit=1)
            found_track = track.get("tracks").get("items")
            if found_track:
                track_uri = track.get("tracks").get("items")[0].get("uri")
                if track_uri not in existing_tracks:
                    log.info("Adding %s" % track_name)
                    new_tracks.append(track_uri)
            else:
                not_found.append(track_name)
    new_tracks = list(set(new_tracks))
    # Add new tracks, if any, to the playlist.
    if new_tracks:
        spotify.user_playlist_add_tracks(user, playlist, new_tracks, position=0)
    if not_found:
        log.warning("Could not find")
        log.warning("\n".join(not_found))


def main(cfg_path):
    cfg = load_config(cfg_path)
    reddit = get_reddit_session(cfg)
    spotify = get_spotify_session(cfg)
    for subreddit in ['metal', 'Music', 'listentothis', 'deephouse']:
        update_playlist(cfg, spotify, reddit, subreddit)
