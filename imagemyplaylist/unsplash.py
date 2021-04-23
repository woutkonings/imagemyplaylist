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
        
        
    def query(self, query, page = 1, per_page = 9):
        
        params = {'page' : page,
                  'per_page' : per_page}
        
        req_url = f'https://api.unsplash.com/search/photos?page=1&query={query}'
        res = requests.get(url=req_url, headers=self.headers, params=params)
        r = res.json()
        
        return r
    
    def query_to_display_urls(self, query_result, size = 'small'):
        
        # for x in query_result['results']:
        #     print(x['alt_description'])
        #     print(x['urls'][size])
            
        return {x['alt_description'] : x['urls'][size] for x in query_result['results']}
    
    def save_pictures(self, url_dict, location):
        
        for name, url in url_dict.items():
            r = requests.get(url, allow_redirects=True)
            open(f'{name}.jpeg', 'wb').write(r.content)
    
if __name__ == "__main__":
    
    
    
    sp = spotify.Spotify()
    playlistId = "4J7qSdpBBzCWO9n3kbQIJg" #Disco playlist with 148 songs    
    df = sp.get_song_df(playlistId)
    query = sp.genre_query(df)
    
    us = Unsplash()
    r = us.query(query)
    q = us.query_to_display_urls(r)
    # us.save_pictures(q, 1)
