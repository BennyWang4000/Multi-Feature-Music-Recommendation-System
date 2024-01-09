import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Spotify API credentials
SPOTIFY_CLIENT_ID = '94dccbe6ffcf40ed9d14b9bb614a3d5c'
SPOTIFY_CLIENT_SECRET = '4cfe542a2f19452cb5a0dc853dec046a'
SPOTIFY_ACCESS_TOKEN = "BQCZKIYiyB_lo48ocm2HR0Z_yQKcahMUObQm4E6VAk7SPdTYYa8O6CJLofOHSEknZYE9qnx4la9-LyVojR4hkHCdlp0i5-JfS4Ls_wm2XhTP_iFimFhs3Hr0KqQf8WkaDWYSFjSAh6cjvAw8xAKYWhZwb2MrucbIQd8j4ltxtMEpVg4HTBj_Xyr1pK1qowhRWNPVRQ" #limited life span

# Genius API credentials
GENIUS_ACCESS_TOKEN = '9CwzBACuChVVUmlDmv5rDsecdyxITuVP4D2syZxrNK4axCNJM8VrsmTcmWiMFG-j'

# Use Spotify API to get track information
def get_spotify_track_info(song_id):
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    headers = {'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}'}
    response = requests.get(url, headers=headers)
    return response.json()

# Search for the song on Genius
def search_genius_song(title, artist):
    url = 'https://api.genius.com/search'
    headers = {'Authorization': f'Bearer {GENIUS_ACCESS_TOKEN}'}
    params = {'q': f'{title} {artist}'}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def check_hits(res):
    remote_song_info = None
    for hit in res['response']['hits']:
        if artist.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break
    remote_song_info = remote_song_info
    return remote_song_info

def get_url(remote_song_info):
    song_url = remote_song_info['result']['url']
    song_url = song_url
    return song_url

def filter_square_brackets(text):
    return re.sub(r'[\[\(][^\]\)]*?[\]\)]', '', text)

def scrape_lyrics(song_url):
    page = requests.get(song_url)
    print(song_url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics1 = html.find("div", class_="lyrics")
    lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-1 kUgSbL")
    if lyrics1:
        lyrics = filter_square_brackets(lyrics1.get_text(separator='\n'))
    elif lyrics2:
        lyrics = filter_square_brackets(lyrics2.get_text(separator='\n'))
    elif lyrics1 == lyrics2 == None:
        lyrics = None
    return lyrics

# Main script
# INPUT_FILEPATH = "rap_non_duplicated.csv"
# OUTPUT_FOLDER = "rap_lyrics"

INPUT_FILEPATH = "blues_non_duplicated.csv"
OUTPUT_FOLDER = "blues_lyrics"

song_ids = pd.read_csv(INPUT_FILEPATH)["spotify_id"].to_numpy()
for i in range(2634,len(song_ids)):
    song_id=song_ids[i]
    spotify_track_info = get_spotify_track_info(song_id)
    title = spotify_track_info['name']
    artist = spotify_track_info['artists'][0]['name']
    print(title, "BY", artist)

    genius_search_result = search_genius_song(title, artist)
    remote_song_info = check_hits(genius_search_result)
    if remote_song_info == None:
        lyrics = None
        print(f"Track {title} is not in the Genius database.")
    else:
        url = get_url(remote_song_info)
        lyrics = scrape_lyrics(url)
        if lyrics == None:
            print(f"Lyrics of track {title} is not in the Genius database.")
        else:
            output_path = OUTPUT_FOLDER + f"/{song_id}.txt"
            with open(output_path, 'w', encoding='utf-8') as file:
                file.write(lyrics)
            print(f"Retrieved track {title} lyrics!")

    
    # print(f"Lyrics for '{title}' by {artist}:\n\n{lyrics}")