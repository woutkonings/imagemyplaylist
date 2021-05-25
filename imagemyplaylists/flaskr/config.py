#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 22:34:10 2021

@author: woutkonings
"""


class Config():
    
    #SPOTIFY_CLIENT_ID  = '3ddb444f64434d81929090cdadd76b3d' #Niels
    #SPOTIFY_CLIENT_SECRET = '2ce0f93bbcf84328830798bbe7f1e014' #Niels
    # SPOTIFY_CLIENT_ID  = '9f60eb0d6eef428da8aa960f14074eda' #Wout int
    # SPOTIFY_CLIENT_SECRET = '9e77a91ab0014354bbef9abd03f0f822' #Wout int
    SPOTIFY_CLIENT_ID  = '4234087547434e9d8975aca70b6d537d' #Wout ext
    SPOTIFY_CLIENT_SECRET = 'd0f6af83441c467c8a1d6ddb61a9e348' #Wout ext
    SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/nl/authorize/?'
    SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
    RESPONSE_TYPE = 'code'   
    HEADER = 'application/x-www-form-urlencoded'
    #Port and callback url can be changed or ledt to localhost:5000
    # PORT = "2604"
    
    #CALLBACK_URL_EXTERNAL = "https://pixify.nielsbos.nl"
    CALLBACK_URL_EXTERNAL = "https://spotify.pics"
    CALLBACK_URL_LOCAL = "http://192.168.1.108:2604" #Niels
    # CALLBACK_URL_LOCAL = "http://127.0.0.1:5000" #Wout
    PATH = "spotify/callback/"
    #Add needed scope from spotify user
    SCOPE = "playlist-modify-private playlist-modify-public user-library-modify user-read-private user-follow-read ugc-image-upload playlist-read-private playlist-read-collaborative"
    #token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
    
    
    UNSPLASH_CLIENT_ID = 'rqFCNGMH1VBusao7nen002IltvlQAfffuBd_5B7k4hM'
    UNSPLASH_CLIENT_SECRET = '0avVm46iEXEzUG5p1UMprygoJJIUSYgAGqScwu2Lnqs'
    
    
    USER_TOKEN = 'BQCX49B8GjXQ_LJs-AHjB3ulA7SewuPZ39c0lJP5GAwa26GrEY9QP8UhYqCR2HNOMbXYMIoA8IBMLgQL_ypvPJIVvHEpv5qObR8SIYsMy50ZZxEjG43mLanJ0kY5Wwuka_F-gMqIs1YoHoNNOmD_LGHzFyOt9qCoAmlx6cYjzPAChEx6g9gq9xbUOAN-PPOIbTMp1vmvvKwKDD407XKaWPSfO2-6eeKv_1msfVsa-9RWAAri8lK6WD-NESI'
    
    QUESTION_SQUARE_URL = 'https://www.iconsdb.com/icons/preview/gray/question-mark-xxl.png'
    
    SEARCH_OPTIONS = ['genre', 'titles', 'artists', 'random']
    
    UNITERESTING_WORDS = ['&', '?', #words that break the code
                          '(feat.', '-', #music specific words
                          #NLTK default stop words
                          'her', 'during', 'among', 'thereafter', 'only', 'hers', 'in', 'none', 'with', 'un', 'put', 'hence', 'each', 'would', 'have', 'to', 'itself', 'that', 'seeming', 'hereupon', 'someone', 'eight', 'she', 'forty', 'much', 'throughout', 'less', 'was', 'interest', 'elsewhere', 'already', 'whatever', 'or', 'seem', 'fire', 'however', 'keep', 'detail', 'both', 'yourselves', 'indeed', 'enough', 'too', 'us', 'wherein', 'himself', 'behind', 'everything', 'part', 'made', 'thereupon', 'for', 'nor', 'before', 'front', 'sincere', 'really', 'than', 'alone', 'doing', 'amongst', 'across', 'him', 'another', 'some', 'whoever', 'four', 'other', 'latterly', 'off', 'sometime', 'above', 'often', 'herein', 'am', 'whereby', 'although', 'who', 'should', 'amount', 'anyway', 'else', 'upon', 'this', 'when', 'we', 'few', 'anywhere', 'will', 'though', 'being', 'fill', 'used', 'full', 'thru', 'call', 'whereafter', 'various', 'has', 'same', 'former', 'whereas', 'what', 'had', 'mostly', 'onto', 'go', 'could', 'yourself', 'meanwhile', 'beyond', 'beside', 'ours', 'side', 'our', 'five', 'nobody', 'herself', 'is', 'ever', 'they', 'here', 'eleven', 'fifty', 'therefore', 'nothing', 'not', 'mill', 'without', 'whence', 'get', 'whither', 'then', 'no', 'own', 'many', 'anything', 'etc', 'make', 'from', 'against', 'ltd', 'next', 'afterwards', 'unless', 'while', 'thin', 'beforehand', 'by', 'amoungst', 'you', 'third', 'as', 'those', 'done', 'becoming', 'say', 'either', 'doesn', 'twenty', 'his', 'yet', 'latter', 'somehow', 'are', 'these', 'mine', 'under', 'take', 'whose', 'others', 'over', 'perhaps', 'thence', 'does', 'where', 'two', 'always', 'your', 'wherever', 'became', 'which', 'about', 'but', 'towards', 'still', 'rather', 'quite', 'whether', 'somewhere', 'might', 'do', 'bottom', 'until', 'km', 'yours', 'serious', 'find', 'please', 'hasnt', 'otherwise', 'six', 'toward', 'sometimes', 'of', 'fifteen', 'eg', 'just', 'a', 'me', 'describe', 'why', 'an', 'and', 'may', 'within', 'kg', 'con', 're', 'nevertheless', 'through', 'very', 'anyhow', 'down', 'nowhere', 'now', 'it', 'cant', 'de', 'move', 'hereby', 'how', 'found', 'whom', 'were', 'together', 'again', 'moreover', 'first', 'never', 'below', 'between', 'computer', 'ten', 'into', 'see', 'everywhere', 'there', 'neither', 'every', 'couldnt', 'up', 'several', 'the', 'i', 'becomes', 'don', 'ie', 'been', 'whereupon', 'seemed', 'most', 'noone', 'whole', 'must', 'cannot', 'per', 'my', 'thereby', 'so', 'he', 'name', 'co', 'its', 'everyone', 'if', 'become', 'thick', 'thus', 'regarding', 'didn', 'give', 'all', 'show', 'any', 'using', 'on', 'further', 'around', 'back', 'least', 'since', 'anyone', 'once', 'can', 'bill', 'hereafter', 'be', 'seems', 'their', 'myself', 'nine', 'also', 'system', 'at', 'more', 'out', 'twelve', 'therein', 'almost', 'except', 'last', 'did', 'something', 'besides', 'via', 'whenever', 'formerly', 'cry', 'one', 'hundred', 'sixty', 'after', 'well', 'them', 'namely', 'empty', 'three', 'even', 'along', 'because', 'ourselves', 'such', 'top', 'due', 'inc', 'themselves']
    
    def set_global(name, x):
        globals()[name] = x
        