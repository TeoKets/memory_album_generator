import os
import requests
from bs4 import BeautifulSoup
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
import dotenv
import pprint
load_dotenv()


# making the html page request
year=input("what year would like to travel?(YYYY-MM-DD)")
class_="c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
response=requests.get(f"https://www.billboard.com/charts/hot-100/{year}",headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"})
response.raise_for_status()

bill_bord_data=response.text

#scraping all the songs
soup=BeautifulSoup(bill_bord_data,"html.parser")
first_title=soup.select("li ul li h3")

#my method for making the top 100 songs into a list :)
top_100_songs_list=[]
mySeperator=" "
for num in range(len(first_title)):
    the_song_in_list=first_title[num].text.split()

    top_100_songs_list.append(mySeperator.join(the_song_in_list))

#authorise my spotify account
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
redirect_uri=os.getenv("REDIRECT_URI")
user_id=os.getenv("USER_ID")
scope = "playlist-modify-private"


sp=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope,
                                             show_dialog=True,
                                             ))
#making the list for inputing into the method to add songs into the playlist
inputing_songs_list=[]
for song in top_100_songs_list:
    try:
        song=sp.search(q=(song,year),limit=1,type="track")
        inputing_songs_list.append(song["tracks"]["items"][0]["external_urls"]["spotify"])
    except :
        print("an error occurred")
playlist=sp.user_playlist_create(user=user_id,name=f"{year}'s TOP 100 HITS",description="ready for nostalgia?",public=False)
playlist_id=playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id,items=inputing_songs_list)
