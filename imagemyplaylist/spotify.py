# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import requests
import config
import base64
import pandas as pd
import numpy as np
import itertools
from statistics import mode


# https://github.com/vanortg/Flask-Spotify-Auth

class Spotify():
    
    def __init__(self):
        
        
        self.client_id = config.SPOTIFY_CLIENT_ID
        self.client_secret =  config.SPOTIFY_CLIENT_SECRET
        self.token = self.get_token(self.client_id, self.client_secret)
        self.headers = {
                        "Authorization": "Bearer " + self.token
                        }
    
    def get_token(self, client_id, client_secret):
        """
        Get API access token
    
        Parameters
        ----------
        client_id : String
            Spotify app client_id
        client_secret : String
            Spotify app secret id
    
        Returns
        -------
        String
            Spotify app access token
    
        """
        # Step 1 - Authorization 
        url = "https://accounts.spotify.com/api/token"
        headers = {}
        data = {}
        
        # Encode as Base64
        message = f"{client_id}:{client_secret}"
        messageBytes = message.encode('ascii')
        base64Bytes = base64.b64encode(messageBytes)
        base64Message = base64Bytes.decode('ascii')
        
        headers['Authorization'] = f"Basic {base64Message}"
        data['grant_type'] = "client_credentials"
        
        r = requests.post(url, headers=headers, data=data)
        token = r.json()['access_token']
        return token
    
    
    def get_playlist(self, playlist_id):
        """
        Get the playlist dictionary
    
        Parameters
        ----------
        playlist_id : TYPE
            DESCRIPTION.
        token : TYPE
            DESCRIPTION.
    
        Returns
        -------
        playlist_dict : TYPE
            DESCRIPTION.
    
        """
        
        playlistUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        
        res = requests.get(url=playlistUrl, headers=self.headers)
        playlist_dict = res.json()
        
        return playlist_dict
    
    def get_playlist_tracks(self, playlist_id):
        """
        Gets all the tracks in a playlist

        Parameters
        ----------
        playlist_id : String
            Spotify playlist ID

        Returns
        -------
        res_list : List
            List of spotify song data

        """
        
        playlistUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
        res_list = []
        
        offset = 0
        list_length = 1
        while list_length != 0:
            params = {'offset' : offset}
            res = requests.get(url=playlistUrl, headers=self.headers, params=params)
            r = res.json()['items']
            list_length = len(r)
            res_list = res_list + r
            offset += 100
        
        return res_list
    
    def get_audio_features(self, song_ids):
        """
        Returns audio features for a list of song IDs

        Parameters
        ----------
        song_ids : List
            list of spotify song IDs

        Returns
        -------
        res_list : List
            List of Json of audio features.

        """
        base_url = 'https://api.spotify.com/v1/audio-features'
        
        start=100
        res_list = []
        list_length = 1
        while list_length != 0:
            songs = song_ids[(start - 100):start]
            text_song_ids = ",".join(songs)
            payload = {'ids' : text_song_ids}
            res = requests.get(url=base_url, headers=self.headers, params=payload)
            r = res.json()['audio_features']
            if r[0] == None:
                break
            list_length = len(r)
            res_list = res_list + r
            start += 100
        
        return res_list
    
    def get_audio_analysis(self, song_id):
        """
        returns the audio analysis for a certain song id
        returns the duration, key, mode and tempo

        Parameters
        ----------
        song_id : String
            Spotify song ID

        Returns
        -------
        output : dictionary
            dictionary of the song features

        """
        #TODO: method comment
        
        req_url = f'https://api.spotify.com/v1/audio-analysis/{song_id}'
        res = requests.get(url=req_url, headers=self.headers)
        r = res.json()['track']
        
        output_features = ['duration', 'key', 'mode', 'tempo']
        output = { key: r[key] for key in output_features}
        return output
    
    
    def get_genres(self, artist_ids):
        """
        Gets the genres for a list of artist ids

        Parameters
        ----------
        artist_ids : List
            List of genre IDs

        Returns
        -------
        res_list : List
            List of list of genres

        """
        
        base_url = 'https://api.spotify.com/v1/artists'
        num_of_artists = len(artist_ids)
        
        #Make artist requests per 50
        res_list = []
        d = int(np.floor(num_of_artists / 50))
        for i in range(1, d + 2):
            query_list = artist_ids[(i-1) * 50 : i * 50]
            text_query_list = ",".join(query_list)
            payload = {'ids' : text_query_list}
            res = requests.get(url=base_url, headers=self.headers, params=payload)
            res_list = res_list + res.json()['artists']
        
        res_list = [x['genres'] for x in res_list]
        
        return res_list
        
    
    def get_song_df(self, playlist_id):
        """
        Creates a dataframe with all the songs in a playlist with various features
        such as artist, artist genres, spotify analysis data etc.

        Parameters
        ----------
        playlist_id : String
            Spotify playlist ID

        Returns
        -------
        df : Pandas Dataframe
            Output Dataframe

        """
        #TODO: method comment
        playlist_dict = self.get_playlist(playlist_id)
        playlist_dict['tracks']['items'] = self.get_playlist_tracks(playlist_id)
        song_ids = [x['track']['id'] for x in playlist_dict['tracks']['items']]
        song_titles = [x['track']['name'] for x in playlist_dict['tracks']['items']]
        song_artists = [x['track']['artists'][0]['name'] for x in playlist_dict['tracks']['items']]
        song_artists_ids = [x['track']['artists'][0]['id'] for x in playlist_dict['tracks']['items']]
        genres = self.get_genres(song_artists_ids)
        
        df = pd.DataFrame()
        df['ID'] = song_ids
        df['Title'] = song_titles
        df['Artist'] = song_artists
        df['ArtistID'] = song_artists
        df['Genres'] = genres
        
        # get the audio features and put in dataframe format
        df_add = pd.DataFrame(index = df.index)
        s = self.get_audio_features(song_ids)
        df_add['feature'] = self.get_audio_features(song_ids)
        df_add = pd.json_normalize(df_add['feature'])
        
        df = pd.concat([df, df_add], axis=1)
        
        return df
    
    def genre_query(self, df):
        """
        gets the most common genres in the dataframe

        Parameters
        ----------
        df : Pandas Dataframe
            Dataframe with the songs and features

        Returns
        -------
        query : String
            String of the genres to query on

        """
        genres = list(df['Genres'])
        merged = list(itertools.chain(*genres))
        query = mode(merged)
        
        return query


if __name__ == "__main__":
    
    
    sp = Spotify()
    spotify_client_id = config.SPOTIFY_CLIENT_ID
    spotify_client_secret = config.SPOTIFY_CLIENT_SECRET
    token = sp.get_token(spotify_client_id, spotify_client_secret)
    
    playlistId = "4J7qSdpBBzCWO9n3kbQIJg" #Disco playlist with 148 songs
    #playlistId = "55oXRfL4wQCPxFMHY3ReFo" # Electro playlist with 31 songs
    
    df = sp.get_song_df(playlistId)
    

    