"""Module providing a function"""
import os
import base64
import json
import webbrowser
import urllib.parse

from requests import post, get
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "http://localhost:7777/callback"
scope = "user-read-private%20user-read-email"

def get_token():
    """Function allowing us to get the token from the spotify API"""
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data, timeout=3.00)
    json_result = json.loads(result.content)
    return_token = json_result["access_token"]
    return return_token

def get_authorize_token():
    """Function allowing us to get an authorized token from the spotify API"""
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    endpoint = "https://accounts.spotify.com/api/token"

    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": "user-read-private user-read-email"
    }
    webbrowser.open("https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(auth_headers))

def get_auth_header(token):
    """Function which constructs a header for post requests"""
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    """Function which searches for an artist"""
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers, timeout=3.00)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None

    return json_result[0]

def get_songs_by_artist(token, artist_id):
    """Function which returns songs by a given artist"""
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=3.00)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_profile(token, user_id):
    """Function which retrieves a profile"""
    url = f"https://api.spotify.com/v1/users/{user_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=3.00)
    return result

def get_current_user(token):
    """Function to retrieve current user"""
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)
    result = get(url, headers=headers, timeout=3.00)
    print(result.content)
   # return json_result

auth_token = get_token()
get_authorize_token()
