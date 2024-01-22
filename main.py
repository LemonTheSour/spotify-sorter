"""Module providing a function"""
import spotipy

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SCOPE = "user-read-private,user-read-email,playlist-modify-public,playlist-modify-private"

# playlist_add_items(playlist_id, items, position=None) ------ Add items to a playlist
# playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode') ------- Get full details of a playlist
# playlist_remove_all_occurrences_of_items(playlist_id, items, snapshot_id=None) --------- Remove items from playlist

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE))
user = sp.current_user()
userID = user["id"]

# playlists = sp.user_playlists(userID)
#print(playlists["items"][0])


def get_user_id():
    """Function to return the ID of the current user"""
    return sp.current_user()["id"]

def get_playlists(user_id):
    """Function to return the target playlists Lucy and Lucille for reorganising"""
    playlists = sp.user_playlists(user_id)["items"]
    target_playlists = []

    for item in playlists:
        if item["name"] == "Lucy" or item["name"] == "Lucille":
            target_playlists.append(item)

    if(target_playlists[0]["name"] == "Lucy"):
        lucy = target_playlists[0]
        lucille = target_playlists[1]
    else:
        lucy = target_playlists[1]
        lucille = target_playlists[0]

    return lucy, lucille

def check_length(playlist):
    """Function for checking the length of a playlist"""
    return playlist["tracks"]["total"]

def get_tracks_to_add(playlist, num):
    """Function for getting a list of track ids in a playlist"""
    playlist_id = playlist["id"]
    tracks_data = sp.playlist_tracks(playlist_id)["items"]
    tracks = []

    for idx, val in enumerate(tracks_data):
        tracks.append(val["track"]["uri"])

    return tracks[:num]

userID = get_user_id()
lucy, lucille = get_playlists(userID)

lucille_length = check_length(lucille)
difference = lucille_length - 50

if difference != 0:
    tracks_to_transfer = get_tracks_to_add(lucille["id"], difference)
    sp.playlist_add_items(lucy["id"], tracks_to_transfer)
    sp.playlist_remove_all_occurrences_of_items(lucy["id"], tracks_to_transfer)
