#!/usr/bin/env python3
"""
generate playlist uses a list of artists to generate a playlist of top tracks 

Use this to create a selection from your favourite festival lineup 

### CHANGE LOG ### 
2020-09-03 Nabil-Fareed Alikhan <nabil@happykhan.com>
    * Initial build - split from dirty scripts
"""
import argparse
import sys
import os
import time
from os import path
import meta
import logging
from spotipy.util import prompt_for_user_token
import spotipy
import yaml


epi = "Licence: " + meta.__licence__ +  " by " +meta.__author__ + " <" +meta.__author_email__ + ">"
logging.basicConfig()
log = logging.getLogger()

def chunks(l, n):
    # For item i in a range that is a length of l,
    for i in range(0, len(l), n):
        # Create an index range for l of n items:
        yield l[i:i+n]

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

def load_config(config_file=path.join(path.expanduser("~"), ".listen.yml")):
    if path.exists('.listen.yml'):
        with open('.listen.yml', "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
            return cfg        
    else:
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

def update_playlist(cfg, spotify, artlist, playlist_name):
    log.info('Building playlist for %s' %playlist_name)
    user = cfg["spotify"]["username"]
    not_found = []
    sum = []
    # Find existing playlist. 
    # Insert or update. 
    playlist_id = get_playlist_id(spotify, user, playlist_name)
    existing_tracks = get_existing_tracks(spotify, user, playlist_id)
    new_tracks = []
    for artist_name in artlist:
        #  add to spotify playlist list if its not in the playlist already
        try:
            artist = spotify.search(artist_name, type="artist", limit=1)
            found_artist = artist.get("artists").get('items')
            if found_artist:
                found_artist_name = found_artist[0].get('name')
                found_artist_id = found_artist[0].get('id')
                track_uris = [track.get('uri') for track in spotify.artist_top_tracks(found_artist_id).get('tracks')] 
                log.info("Adding %s to %s" % (found_artist_name, playlist_name))
                for track_uri in track_uris[0:args.track_number]:
                    if track_uri not in existing_tracks:
                        new_tracks.append(track_uri)
            else:
                not_found.append(artist_name)
        except ConnectionError:
            log.warning("ConnectionError")

    new_tracks = f7(new_tracks)
    # Add new tracks, if any, to the playlist.
    if new_tracks:
        for chunk in chunks(new_tracks, 99):
            spotify.user_playlist_add_tracks(user, playlist_id, chunk)
    sum.append([playlist_name, playlist_id])
    if not_found:
        log.warning("\nCould not find following for %s:" % playlist_name)
        log.warning("\n".join(list(set(not_found))))
    return sum


def main(args): 
    # fetch list of artists from file. 
    playlist_name = [line for line in open(args.listfile).readlines() if line.startswith('#')] 
    if playlist_name:
        playlist_name = playlist_name[0][1:].strip()
    else:
        playlist_name = args.listfile
    artlist = [line for line in open(args.listfile).readlines() if not line.startswith('#') and len(line) > 3 ] 
    # Do lookup for top two tracks 
    cfg = load_config(args.config_file)
    spotify = get_spotify_session(cfg)
    update_playlist(cfg, spotify, artlist, playlist_name)

if __name__ == '__main__':
    start_time = time.time()
    log.setLevel(logging.INFO)
    desc = __doc__.split('\n\n')[1].strip()
    parser = argparse.ArgumentParser(description=desc,epilog=epi)
    parser.add_argument ('-v', '--verbose', action='store_true', default=False, help='verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s ' + meta.__version__)
    parser.add_argument("--config_file", default=path.join(path.expanduser("~"), ".listen.yml"), help="Path of config file")
    parser.add_argument("--track_number", default=2, help="Number of tracks to add")
    parser.add_argument('listfile', action='store', help='File list of files')
    args = parser.parse_args()
    if args.verbose: 
        log.setLevel(logging.DEBUG)
        log.debug( "Executing @ %s\n"  %time.asctime())    
    main(args)
    if args.verbose: 
        log.debug("Ended @ %s\n"  %time.asctime())
        log.debug('total time in minutes: %d\n' %((time.time() - start_time) / 60.0))
    sys.exit(0)