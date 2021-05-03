#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:34:10 2021

@author: woutkonings
"""


class Config():
    
    SPOTIFY_CLIENT_ID  = '9f60eb0d6eef428da8aa960f14074eda'
    SPOTIFY_CLIENT_SECRET = '9e77a91ab0014354bbef9abd03f0f822'
    SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/nl/authorize/?'
    SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
    RESPONSE_TYPE = 'code'   
    HEADER = 'application/x-www-form-urlencoded'
    #Port and callback url can be changed or ledt to localhost:5000
    PORT = "5000"
    CALLBACK_URL = "http://127.0.0.1"
    PATH = "spotify/callback/"
    #Add needed scope from spotify user
    SCOPE = "playlist-modify-private playlist-modify-public user-library-modify user-read-private user-follow-read ugc-image-upload"
    #token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
    
    
    UNSPLASH_CLIENT_ID = 'rqFCNGMH1VBusao7nen002IltvlQAfffuBd_5B7k4hM'
    UNSPLASH_CLIENT_SECRET = '0avVm46iEXEzUG5p1UMprygoJJIUSYgAGqScwu2Lnqs'
    
    
    USER_TOKEN = 'BQB1bQnGv3zWQFIBbXfqBOiILqwPfc0yc_zGSx4hMsFo7wdBmFDH4zLW8Pjb6S5JhVHgnnglBbuqM9M8eC_CerEW78udALBKFZycsxeuLnjGdtcSgAuOtr0z7fBTg76jacN-AQCUNWmLZrx39E9QhJhFuuUX5VziPVBFQNf_7qaHbpy8_MTZ2CgqhLdNiarRoTwRI1nzcGsByh2VfK8DOP-_e6FqFO--nt-LjUMhS0GTJw'
    
    def set_global(name, x):
        globals()[name] = x