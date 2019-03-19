==================
listentoeverything
==================

.. image:: https://travis-ci.org/happykhan/listentoeverything.svg?branch=master
        :target: https://travis-ci.org/happykhan/listentoeverything
.. image:: https://img.shields.io/pypi/v/listentoeverything.svg
        :target: https://pypi.python.org/pypi/listentoeverything
        :alt: Pypi
.. image:: https://pyup.io/repos/github/happykhan/listentoeverything/shield.svg
        :target: https://pyup.io/repos/github/happykhan/listentoeverything/
        :alt: Updates


I’m always looking for new music. I found an applet on `IFTTT`_, which
didn’t work. It couldn’t handle posts other than “Artist - Title”. So I
wrote my own and put it up on `Github`_. Here are some specifics:

-  `Reddit`_ is social media site where users post material, which is
   voted for or against by others. The higher the vote, the higher the
   prominence of the material
-  There are many specific channels (subreddits) for different Music
   genres; We can use these lists to make curated playlists.
-  Playlist are based on either the ‘top’ posts or ‘hot’ posts lists
   e.g. \ `/r/music top of the week`_
-  I use `Spotipy`_ and `PRAW`_ for talking to Spotify and Reddit.
-  The program cleans the list up with custom parser.
-  Each playlist are limited to 100 songs. As new songs are added, the
   oldest ones are removed.
-  I update the playlists every day.

See the results at https://happykhan.com/playlists/

Installation and Usage
----------------------
via pip:
~~~~~~~~~~
.. code-block:: bash

    pip install listentoeverything

via source:
~~~~~~~~~~~
.. code-block:: bash

    git clone git@github.com:happykhan/listentoeverything.git
    cd listentoeverything
    pip install -r requirements.txt

Then run:
~~~~~~~~~

.. code-block:: bash

    python listentoeverything/cli.py --config_file <config_file.yml>


Configuration
-------------
You will need to sign up to the Spotify API and reddit API.

* https://developer.spotify.com/documentation/web-api/
* https://www.reddit.com/dev/api/

They will issue you with various authorisation keys which you need to
specify in the config file (default location is ~/.listen).

.. code-block:: yaml

    reddit:
       client_id: <Your key>
       client_secret: <Your key>
       user_agent: listenonspotify
       username: <Your reddit username>
       password: <Your pass>
    spotify:
       username: <Your spotify username>
       scope: playlist-modify-public
       client_id: <Your key>
       client_secret: <Your key>
       redirect_uri: http://localhost/



Spotify login
-------------
Spotify requires users to authorise 3rd party programs through the website.
Normally the first time you run this script it will open a web browser and redirect you
to spotify, where a user would need to click authorise. Then it will come back to
a redirect URL. As this isn't a website, I just send it back to localhost.

.. image:: docs/spotify_login.png

The script will want to know what the URL was, including the code. So copy this
from the address bar and paste in the prompt.

.. image:: docs/spotify_token.png

The token will be cached for a while so you do not need to do this every time.


License
-------
listentoeverything is free software under the GNU General Public License v3.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _IFTTT: https://ifttt.com/applets/X9h3Mnmd-automatically-add-the-top-posts-from-the-r-listentothis-subreddit-to-a-spotify-playlist
.. _Github: https://github.com/happykhan/listentoeverything/
.. _Reddit: http://reddit.com
.. _/r/music top of the week: https://www.reddit.com/r/music/top/?t=week
.. _Spotipy: https://spotipy.readthedocs.io/en/latest/
.. _PRAW: https://praw.readthedocs.io/en/latest/
