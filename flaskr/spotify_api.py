# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import base64, json, requests
from flaskr.config import Config
import pandas as pd
import numpy as np
import itertools
from statistics import mode


# https://github.com/vanortg/Flask-Spotify-Auth

class Spotify():
    
    def __init__(self):
        
        
        self.client_id = Config.SPOTIFY_CLIENT_ID
        self.client_secret =  Config.SPOTIFY_CLIENT_SECRET
        self.token = self.get_token(self.client_id, self.client_secret)
        self.token_data = []
        self.refresh_token = ''
        self.headers = {
                        "Authorization": "Bearer " + self.token
                        }
    
    # CODE FOR AUTHORISATIONS
    
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
    
    def getAuth(self, client_id, redirect_uri, scope):
        data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(Config.SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
        return data

    def getToken(self, code, client_id, client_secret, redirect_uri):
        body = {
            "grant_type": 'authorization_code',
            "code" : code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }
        # Encode as Base64
        message = f"{client_id}:{client_secret}"
        messageBytes = message.encode('ascii')
        base64Bytes = base64.b64encode(messageBytes)
        base64Message = base64Bytes.decode('ascii')
        
        headers = {"Content-Type" : Config.HEADER, "Authorization" : f"Basic {base64Message}"} 
        post = requests.post(Config.SPOTIFY_URL_TOKEN, params=body, headers=headers)
        print(post.text)
        return self.handleToken(json.loads(post.text))
    
    
    def handleToken(self, response):
        auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
        self.refresh_token = response["refresh_token"]
        print(str([response["access_token"], auth_head, response["scope"], response["expires_in"]]))
        return [response["access_token"], auth_head, response["scope"], response["expires_in"]]
    
    
    def refreshAuth(self):
        body = {
            "grant_type" : "refresh_token",
            "refresh_token" : self.refresh_token
        }
    
        post_refresh = requests.post(Config.SPOTIFY_URL_TOKEN, data=body, headers=Config.HEADER)
        p_back = json.dumps(post_refresh.text)
        
        return self.handleToken(p_back)
    
    
    def getUser(self):
        return self.getAuth(self.client_id, "{}:{}/{}".format(Config.CALLBACK_URL, Config.PORT, Config.PATH), Config.SCOPE)
    
    def getUserToken(self, code):
        self.token_data = self.getToken(code, self.client_id, self.client_secret, "{}:{}/{}".format(Config.CALLBACK_URL, Config.PORT, Config.PATH))
     
    def refreshToken(self, time):
        time.sleep(time)
        self.token_data = self.refreshAuth()
    
    def getAccessToken(self):
        return self.token_data
    
    def getUserInfo(self, userToken):
        
        headers = {
                        "Authorization": "Bearer " + userToken
                        }
        
        userUrl =  'https://api.spotify.com/v1/me'
        
        res = requests.get(url=userUrl, headers=headers)
        return res.json()
    
    def getUserPlaylists(self, userToken):
        
        
        
        headers = {
                        "Authorization": "Bearer " + userToken
                        }
        
        userUrl =  'https://api.spotify.com/v1/me/playlists'
        
        res = requests.get(url=userUrl, headers=headers)
        return res.json()
    
    # CODE FOR QUERIES
    
    def get_playlist(self, playlist_id, token=None):
        """
        Get the playlist dictionary
    
        Parameters
        ----------
        playlist_id : TYPE
            DESCRIPTION.
        token : String
            Spotify access token. Default is the instance app token.
    
        Returns
        -------
        playlist_dict : TYPE
            DESCRIPTION.
    
        """
        if token is None:
            token = self.token
        headers = {
                        "Authorization": "Bearer " + token
                        }
        
        playlistUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}"
        
        res = requests.get(url=playlistUrl, headers=headers)
        playlist_dict = res.json()
        
        return playlist_dict
    
    def get_playlist_tracks(self, playlist_id, token = None):
        """
        Gets all the tracks in a playlist

        Parameters
        ----------
        playlist_id : String
            Spotify playlist ID
        token : String
            Spotify access token. Default is the instance app token.

        Returns
        -------
        res_list : List
            List of spotify song data

        """
        
        if token is None:
            token = self.token
        headers = {
                        "Authorization": "Bearer " + token
                        }
        
        playlistUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
        res_list = []
        
        offset = 0
        list_length = 1
        while list_length != 0:
            params = {'offset' : offset}
            res = requests.get(url=playlistUrl, headers=headers, params=params)
            r = res.json()['items']
            list_length = len(r)
            res_list = res_list + r
            offset += 100
        
        return res_list
    
    def get_audio_features(self, song_ids, token = None):
        """
        Returns audio features for a list of song IDs

        Parameters
        ----------
        song_ids : List
            list of spotify song IDs
        token : String
            Spotify access token. Default is the instance app token.

        Returns
        -------
        res_list : List
            List of Json of audio features.

        """
        base_url = 'https://api.spotify.com/v1/audio-features'
        
        if token is None:
            token = self.token
        headers = {
                        "Authorization": "Bearer " + token
                        }
        
        start=100
        res_list = []
        list_length = 1
        while list_length != 0:
            songs = song_ids[(start - 100):start]
            text_song_ids = ",".join(songs)
            payload = {'ids' : text_song_ids}
            res = requests.get(url=base_url, headers=headers, params=payload)
            r = res.json()['audio_features']
            if r[0] == None:
                break
            list_length = len(r)
            res_list = res_list + r
            start += 100
        
        return res_list
    
    def get_audio_analysis(self, song_id, token = None):
        """
        returns the audio analysis for a certain song id
        returns the duration, key, mode and tempo

        Parameters
        ----------
        song_id : String
            Spotify song ID
        token : String
            Spotify access token. Default is the instance app token.

        Returns
        -------
        output : dictionary
            dictionary of the song features

        """
        
        if token is None:
            token = self.token
        headers = {
                        "Authorization": "Bearer " + token
                        }
        
        req_url = f'https://api.spotify.com/v1/audio-analysis/{song_id}'
        res = requests.get(url=req_url, headers=headers)
        r = res.json()['track']
        
        output_features = ['duration', 'key', 'mode', 'tempo']
        output = { key: r[key] for key in output_features}
        return output
    
    
    def get_genres(self, artist_ids, token=None):
        """
        Gets the genres for a list of artist ids

        Parameters
        ----------
        artist_ids : List
            List of genre IDs
        token : String
            Spotify access token. Default is the instance app token.

        Returns
        -------
        res_list : List
            List of list of genres

        """
        
        if token is None:
            token = self.token
        headers = {
                        "Authorization": "Bearer " + token
                        }
        
        base_url = 'https://api.spotify.com/v1/artists'
        num_of_artists = len(artist_ids)
        
        #Make artist requests per 50
        res_list = []
        d = int(np.floor(num_of_artists / 50))
        for i in range(1, d + 2):
            query_list = artist_ids[(i-1) * 50 : i * 50]
            text_query_list = ",".join(query_list)
            payload = {'ids' : text_query_list}
            res = requests.get(url=base_url, headers=headers, params=payload)
            if 'artists' in res.json():
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
        token : String
            Spotify access token. Default is the instance app token.

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
    spotify_client_id = Config.SPOTIFY_CLIENT_ID
    spotify_client_secret = Config.SPOTIFY_CLIENT_SECRET
    token = sp.get_token(spotify_client_id, spotify_client_secret)
    
    #playlistId = "4J7qSdpBBzCWO9n3kbQIJg" #Disco playlist with 148 songs
    playlistId = "55oXRfL4wQCPxFMHY3ReFo" # Electro playlist with 31 songs
    
    playlists = sp.getUserPlaylists(Config.USER_TOKEN)
    
    df = sp.get_song_df(playlistId)
    

    