import json
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import pprint

CLIENT_ID = "f449728d0b434b20b3ace7283538287a"
CLIENT_SECRET = "6e39fb85ba9348429ebf2a5506e73ad4"
URI = "https://example.com"
SPOTIFY_USER = "31iwu7clmiawsyltsf3ypxi3g4eu"
SCOPE = 'user-library-read'
CACHE = '.spotipyoauthcache'
AUTHORIZATION_TOKEN = "BQDCDMzydgz-y4JtgfaJ6BIWx998C0IIhwZ_EwiCPqqFSVeZNbabcQlF_VHVg6kaLEAhyInL4-k7YvGkl40NbBOS_w1akkFkh2epeXWVM9S-ovqXThduwpEUyAhrEw1R_qq7UwZguziGFvUY7uxNW_8_Fyw1QL2s9-gGg8F01myitnN8W5CHaqx7QrEeZUsO77cUFWBQS7QHIyHaAlJJCb5bWS7kDuj8ffUcPQ"


# Getting songs from User's given Year

songs_data = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{songs_data}")
song_response = response.text
soup = BeautifulSoup(song_response, "html.parser")
song = soup.select("li ul li h3")
song_list = [i.getText().strip() for i in song]
year = songs_data.split("-")[0]


# Getting Authorization,Access Token from Spotipy

# S_A = spotipy.oauth2.SpotifyOAuth(client_id=CLIENT_ID,
#                                   client_secret=CLIENT_SECRET,
#                                   redirect_uri=URI,
#                                   scope="playlist-modify-private",
#                                   cache_path="token.txt",
#                                   show_dialog=True)
# S_A.get_access_token()


# Getting user details from spotipy

user = spotipy.client.Spotify(auth=AUTHORIZATION_TOKEN)
user_data = user.current_user()
user_id = user_data["id"]
songs_uri_list = []
for track in song_list:
    try:
        result = (user.search(q=f"track{track} year2003", type="track"))
        song_uri = (result["tracks"]["items"][0]["uri"])
        songs_uri_list.append(song_uri)

    except IndexError:
        print(f"{track} song does\'nt exist. Song skipped")


# Creating a Playlist

data = {
    "name": f"{songs_data} Billboard 100",
    "description": f"Top Songs from {songs_data}",
    "public": False
}

headers = {
    "Authorization": f"Bearer {AUTHORIZATION_TOKEN}",
    "Content-Type": "application/json"

}

response = requests.post(url=f"https://api.spotify.com/v1/users/{user_id}/playlists", data=json.dumps(data), headers=headers)
PPrint = pprint.PrettyPrinter()
playlist_data = (response.json())
playlist_id = playlist_data["id"]
param = {
    "uris": songs_uri_list,
    "position": 0
}
Add_song = requests.post(url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks",
                         data=json.dumps(param),
                         headers=headers)
print(f"Playlist for the given time ({songs_data}) has been created successfully.")

