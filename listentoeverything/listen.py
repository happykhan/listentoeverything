# -*- coding: utf-8 -*-

"""Main module."""
import logging
import spotipy
import yaml
from spotipy.util import prompt_for_user_token
from os import path
from requests.exceptions import ConnectionError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


def load_config(config_file=path.join(path.expanduser("~"), ".listen.yml")):
    with open(config_file, "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        return cfg


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


def get_playlist_id(spotify, user, playlist_name):
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
    return playlist


def get_existing_tracks(spotify, user, playlist):
    # Find existing tracks, save the URI
    existing_tracks = spotify.user_playlist_tracks(user, playlist)
    if existing_tracks:
        existing_tracks = [
            x.get("track").get("uri") for x in existing_tracks.get("items")
        ]
    else:
        existing_tracks = []
    return existing_tracks


def my_import(name):
    m = __import__(name)
    for n in name.split(".")[1:]:
        m = getattr(m, n)
    return m


def update_playlist(cfg, spotify, subreddit_name):
    log.info('Building playlist for %s' %subreddit_name)
    try:
        parse = getattr(my_import('parsers.%s' % subreddit_name), subreddit_name.title())(subreddit_name, cfg)
    except ModuleNotFoundError:
        log.info('Parser not found, using generic for %s' % subreddit_name)
        parse = getattr(my_import('parsers.generic'), 'Generic')(subreddit_name, cfg)
    playlists = parse.get_playlist()
    with open('../tests/%s-sample.txt' % subreddit_name, 'w') as test_data:
        test_data.write('\n'.join(parse.get_test_data()))
    user = cfg["spotify"]["username"]
    not_found = []
    sum = []
    for playlist_name, track_names in playlists.items():
        playlist_id = get_playlist_id(spotify, user, playlist_name)
        existing_tracks = get_existing_tracks(spotify, user, playlist_id)
        new_tracks = []
        #  add to spotify playlist list if its not in the playlist already
        for track_name in track_names:
            try:
                track = spotify.search(track_name, type="track", limit=1)
                found_track = track.get("tracks").get("items")
                if found_track:
                    track_uri = track.get("tracks").get("items")[0].get("uri")
                    if track_uri not in existing_tracks:
                        log.info("Adding %s to %s" % (track_name, playlist_name))
                        new_tracks.append(track_uri)
                else:
                    not_found.append(track_name)
            except ConnectionError:
                log.warning("ConnectionError")

        new_tracks = list(set(new_tracks))
        # Add new tracks, if any, to the playlist.
        if new_tracks:
            spotify.user_playlist_add_tracks(user, playlist_id, new_tracks[:99], position=0)
        current_tracks = new_tracks + existing_tracks
        if len(current_tracks) > 100:
            spotify.user_playlist_remove_all_occurrences_of_tracks(user, playlist_id, current_tracks[100:])
        sum.append([playlist_name, playlist_id])
    if not_found:
        log.warning("\nCould not find following for %s:" % subreddit_name)
        log.warning("\n".join(list(set(not_found))))
    return sum


def main(cfg_path):
    cfg = load_config(cfg_path)
    spotify = get_spotify_session(cfg)
    with open(cfg.get('summary_path'), 'w') as sum_file:
        sum_file.write("| Playlist name | URL | Description |\n")
        sum_file.write("| --- | --- | --- |\n")
        for subreddit in cfg.get('subreddits'):
            sum = update_playlist(cfg, spotify, subreddit)
            for s in sum:
                description = 'Automated playlist'
                playlist_url = 'https://open.spotify.com/playlist/%s' % s[1]
                sum_file.write("|{}|[Spotify playlist]({})|{}|\n".format(s[0], playlist_url, description))
                sum_file.flush()


