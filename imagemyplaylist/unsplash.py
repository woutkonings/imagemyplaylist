#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 00:05:12 2021

@author: woutkonings
"""

import requests
import config
import base64
import pandas as pd
import spotify


class Unsplash():
    
    def __init__(self):
        
        self.client_id = config.UNSPLASH_CLIENT_ID
        self.client_secret = config.UNSPLASH_CLIENT_SECRET
        
        self.headers = {
                        "Authorization": "Client-ID " + self.client_id
                        }
        
        
    def query(self, query):
        
        req_url = f'https://api.unsplash.com/search/photos?page=1&query={query}'
        res = requests.get(url=req_url, headers=self.headers)
        r = res.json()
        
        return r

if __name__ == "__main__":
    
    
    
    sp = spotify.Spotify()
    playlistId = "4J7qSdpBBzCWO9n3kbQIJg" #Disco playlist with 148 songs    
    df = sp.get_song_df(playlistId)
    query = sp.genre_query(df)
    
    us = Unsplash()
    r = us.query(query)
