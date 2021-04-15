# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import requests
import config
import base64
import pandas as pd


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
    
    playlistUrl = f"https://api.spotify.com/v1/playlists/{playlistId}"
    headers = {
    "Authorization": "Bearer " + token
    }
    
    res = requests.get(url=playlistUrl, headers=headers)
    playlist_dict = res.json()
    
    return playlist_dict

def get_songs_feature(playlist_dict, feature):
    
    return [x['track'][feature] for x in playlist_dict['tracks']['items']]

def get_audio_features(song_ids, token):
    
    headers = {
    "Authorization": "Bearer " + token
    }
    
    # audio_feature_url = 'https://api.spotify.com/v1/audio-features' + '?ids=' + "%".join(song_ids)
    base_url = 'https://api.spotify.com/v1/audio-features'
    text_song_ids = ",".join(song_ids)
    payload = {'ids' : text_song_ids}
    
    #TODO: Waarom werkt deze tori niet....
    res = requests.get(url=base_url, headers=headers, params=payload)
    r = res.json()
    return r

def get_audio_analysis(song_id, token):
    
    
    headers = {
    "Authorization": "Bearer " + token
    }
    
    req_url = f'https://api.spotify.com/v1/audio-analysis/{song_id}'
    res = requests.get(url=req_url, headers=headers)
    r = res.json()['track']
    
    output_features = ['duration', 'key', 'mode', 'tempo']
    output = { key: r[key] for key in output_features}
    return output

if __name__ == "__main__":
    
    spotify_client_id = config.SPOTIFY_CLIENT_ID
    spotify_client_secret = config.SPOTIFY_CLIENT_SECRET
    token = get_token(spotify_client_id, spotify_client_secret)
    config.set_global('TOKEN', token)
    
    playlistId = "66yuBIG6Ko7topxRJ1b3iq"
    playlist_dict = get_playlist(playlistId, config.TOKEN)
    tracks = playlist_dict['tracks']['items'][0]['track']
    song_ids = get_songs_feature(playlist_dict, 'id')
    song_titles = get_songs_feature(playlist_dict, 'name')
    song_artists = [x[0]['name'] for x in get_songs_feature(playlist_dict, 'artists')]
    
    df = pd.DataFrame()
    df['ID'] = song_ids
    df['Title'] = song_titles
    df['Artist'] = song_artists
    
    df2 = pd.DataFrame()
    df2['analysis'] = df['ID'].apply(lambda x : get_audio_analysis(x, config.TOKEN))
    d = pd.json_normalize(df2['analysis'])
    
    df = pd.concat([df, d], axis=1)
    