from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

# loading environment variables
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

## TRACK LIST
# the number of tracks for each artist
numTracks = 10

f = open("artist.txt", "r")     # opening the file in read mode
d = f.read()                    # reading the file

# formatting the list of the file
artist_list = d.split("\n")
# deleting any blank lines
artist_list = [x for x in artist_list if x]

# retrieving spotify token
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url,headers=headers,data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# retrieving unique artist ID
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists..")
        return None
    return json_result[0]

# get list of artist IDs
def get_artist_id_list(token, artist_list):
    artist_id_list = [None]*len(artist_list)

    for count in range(len(artist_list)):
       result = search_for_artist(token, artist_list[count])
       artist_id_list[count] = result["id"]
    return artist_id_list

# get songs by artist
def get_songs_by_artist(token, artist_id, num):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA" 
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result[0:num]

# get list of track IDs
def get_track_id_list(token, artist_id_list, num):
    track_id_list = [None]*len(artist_id_list)*num      # create list to store track IDs, sized by list of artists and number of tracks requested from each artist
    track_name_list = [None]*len(artist_id_list)*num      # create list to store track names, sized by list of artists and number of tracks requested from each artist
    trackIndex = 0                                      # setting track index to 0

    for count in range(len(artist_id_list)):
        songs = get_songs_by_artist(token, artist_id_list[count], num)
        for idx, song in enumerate(songs):
            track_id_list[trackIndex] = song['id']
            track_name_list[trackIndex] = song['name']
            trackIndex += 1
    return track_id_list, track_name_list

token = get_token()
artist_id_list = get_artist_id_list(token, artist_list)
print(get_track_id_list(token, artist_id_list, numTracks))

def track_popularity(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA" 
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
