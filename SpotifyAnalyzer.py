import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class Processor():
    def __init__(self):
        self.dir_path = "/users/carolinejung/spotify-2016-2024/"
        self.filepath = "1-raw-data/cleaned_data.csv"
        self.id = os.getenv("SPOTIFY_CLIENT_ID")
        self.secret = os.getenv("SPOTIFY_CLIENT_SECRET")

    def read_clean_csv(self):
        data = pd.read_csv(self.dir_path + self.filepath, index_col=0)
        data = data.drop(['username','conn_country','ip_addr_decrypted', 'user_agent_decrypted','episode_name',
                          'episode_show_name', 'spotify_episode_uri', 'reason_start', 'offline', 'offline_timestamp',
                          'incognito_mode'], axis=1)
        return data
    
    def get_skipped_tracks(self):
        # possible TODO: perhaps make this more general?
        data = self.read_clean_csv() # full data
        skipped = data[data["skipped"]==True] # skipped tracks
        count_series = skipped.groupby("spotify_track_uri").size().to_frame("count") # count how many times it gets skipped
        skipped_summary = pd.merge(skipped.drop_duplicates(["spotify_track_uri"]), count_series, on="spotify_track_uri")
        return skipped_summary.sort_values("count", ascending=False)
    
    def client(self):
        """Client for connecting to Spotify API (via spotipy module)"""
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials())