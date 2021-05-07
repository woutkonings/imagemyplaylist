#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:34:10 2021

@author: woutkonings
"""


class Config():
    
    # SPOTIFY_CLIENT_ID  = '3ddb444f64434d81929090cdadd76b3d' #Niels
    # SPOTIFY_CLIENT_SECRET = '2ce0f93bbcf84328830798bbe7f1e014' #Niels
    SPOTIFY_CLIENT_ID  = '9f60eb0d6eef428da8aa960f14074eda' #Wout
    SPOTIFY_CLIENT_SECRET = '9e77a91ab0014354bbef9abd03f0f822' #Wout
    SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/nl/authorize/?'
    SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
    RESPONSE_TYPE = 'code'   
    HEADER = 'application/x-www-form-urlencoded'
    #Port and callback url can be changed or ledt to localhost:5000
    # PORT = "2604"
    CALLBACK_URL_EXTERNAL = "https://pixify.nielsbos.nl"
    # CALLBACK_URL_LOCAL = "http://192.168.1.108:2604" #Niels
    CALLBACK_URL_LOCAL = "http://127.0.0.1:5000" #Wout
    PATH = "spotify/callback/"
    #Add needed scope from spotify user
    SCOPE = "playlist-modify-private playlist-modify-public user-library-modify user-read-private user-follow-read ugc-image-upload playlist-read-private playlist-read-collaborative"
    #token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
    
    
    UNSPLASH_CLIENT_ID = 'rqFCNGMH1VBusao7nen002IltvlQAfffuBd_5B7k4hM'
    UNSPLASH_CLIENT_SECRET = '0avVm46iEXEzUG5p1UMprygoJJIUSYgAGqScwu2Lnqs'
    
    
    USER_TOKEN = 'BQCX49B8GjXQ_LJs-AHjB3ulA7SewuPZ39c0lJP5GAwa26GrEY9QP8UhYqCR2HNOMbXYMIoA8IBMLgQL_ypvPJIVvHEpv5qObR8SIYsMy50ZZxEjG43mLanJ0kY5Wwuka_F-gMqIs1YoHoNNOmD_LGHzFyOt9qCoAmlx6cYjzPAChEx6g9gq9xbUOAN-PPOIbTMp1vmvvKwKDD407XKaWPSfO2-6eeKv_1msfVsa-9RWAAri8lK6WD-NESI'
    
    QUESTION_SQUARE_URL = 'https://www.iconsdb.com/icons/preview/gray/question-mark-xxl.png'
    
    SEARCH_OPTIONS = ['genre', 'titles', 'artists', 'random']
    
    def set_global(name, x):
        globals()[name] = x
        