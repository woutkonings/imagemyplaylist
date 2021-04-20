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


# https://github.com/vanortg/Flask-Spotify-Auth


def get_token(client_id, client_secret):
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


def get_playlist(playlist_id, token):
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
    headers = {
    "Authorization": "Bearer " + token
    }
    
    res = requests.get(url=playlistUrl, headers=headers)
    playlist_dict = res.json()
    
    return playlist_dict

def get_playlist_tracks(playlist_id, token):
    #TODO: method comment
    
    playlistUrl = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
    "Authorization": "Bearer " + token
    }
    
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


def get_songs_feature(playlist_dict, feature):
    #TODO: method comment
    return [x['track'][feature] for x in playlist_dict['tracks']['items']]

def get_audio_features(song_ids, token):
    #TODO: method comment
    
    headers = {
    "Authorization": "Bearer " + token
    }
    
    # audio_feature_url = 'https://api.spotify.com/v1/audio-features' + '?ids=' + "%".join(song_ids)
    base_url = 'https://api.spotify.com/v1/audio-features'
    text_song_ids = ",".join(song_ids)
    payload = {'ids' : text_song_ids}
    
    #TODO: Ik heb een vermoeden dat deze ook niet meer dan 100 nummers als input kan nemen
    res = requests.get(url=base_url, headers=headers, params=payload)
    r = res.json()
    return r['audio_features']

def get_audio_analysis(song_id, token):
    #TODO: method comment
    
    headers = {
    "Authorization": "Bearer " + token
    }
    
    req_url = f'https://api.spotify.com/v1/audio-analysis/{song_id}'
    res = requests.get(url=req_url, headers=headers)
    r = res.json()['track']
    
    output_features = ['duration', 'key', 'mode', 'tempo']
    output = { key: r[key] for key in output_features}
    return output


def get_genres(artist_ids, token):
    #TODO: method comment
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
        res_list = res_list + res.json()['artists']
    
    res_list = [x['genres'] for x in res_list]
    
    return res_list
    

def get_song_df(playlist_id, token):
    #TODO: method comment
    playlist_dict = get_playlist(playlist_id, token)
    playlist_dict['tracks']['items'] = get_playlist_tracks(playlist_id, token)
    song_ids = [x['track']['id'] for x in playlist_dict['tracks']['items']]
    song_titles = [x['track']['name'] for x in playlist_dict['tracks']['items']]
    song_artists = [x['track']['artists'][0]['name'] for x in playlist_dict['tracks']['items']]
    song_artists_ids = [x['track']['artists'][0]['id'] for x in playlist_dict['tracks']['items']]
    genres = get_genres(song_artists_ids, token)
    
    df = pd.DataFrame()
    df['ID'] = song_ids
    df['Title'] = song_titles
    df['Artist'] = song_artists
    df['ArtistID'] = song_artists
    df['Genres'] = genres
    
    # get the audio features and put in dataframe format
    df_add = pd.DataFrame(index = df.index)
    s = get_audio_features(song_ids, token)
    df_add['feature'] = get_audio_features(song_ids, token)
    df_add = pd.json_normalize(df_add['feature'])
    
    df = pd.concat([df, df_add], axis=1)
    
    return df

if __name__ == "__main__":
    
    spotify_client_id = config.SPOTIFY_CLIENT_ID
    spotify_client_secret = config.SPOTIFY_CLIENT_SECRET
    token = get_token(spotify_client_id, spotify_client_secret)
    config.set_global('TOKEN', token)
    
    # playlistId = "4J7qSdpBBzCWO9n3kbQIJg" #Disco playlist with 148 songs
    playlistId = "55oXRfL4wQCPxFMHY3ReFo" # Electro playlist with 31 songs
    
    df = get_song_df(playlistId, config.TOKEN)
    

    