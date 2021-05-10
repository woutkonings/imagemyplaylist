#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 00:05:12 2021

@author: woutkonings
"""

import requests
from flaskr.config import Config
import base64
import pandas as pd
from flaskr.spotify_api import Spotify


class Unsplash():
    
    def __init__(self):
        
        self.client_id = Config.UNSPLASH_CLIENT_ID
        self.client_secret = Config.UNSPLASH_CLIENT_SECRET
        self.headers = {
                        "Authorization": "Client-ID " + self.client_id
                        }
        
    def query(self, query, page = 1, per_page = 9):
        """
        Performs an Unsplash query based on a string

        Parameters
        ----------
        query : String
            String to query
        page : int, optional
            The page of the query to request. The default is 1.
        per_page : int, optional
            number of pictures per page to request. The default is 9.

        Returns
        -------
        r : Dictionary
            result of the Unsplash query request

        """
        params = {'query': query,
                  'page' : page,
                  'per_page' : per_page}
        
        req_url = f'https://api.unsplash.com/search/photos'
        res = requests.get(url=req_url, headers=self.headers, params=params)
        r = res.json()
        print()
        return r
    
    def query_to_display_urls(self, query_result, dimension = 400):
        """
        Parameters
        ----------
        query_result : Dictionary
            Json result of the Unsplash API query request
        size : String, optional
            The size of the pictures to get. The default is 'small'. Options:
                full, raw, regular, small, thumb

        Returns
        -------
        dict
            dictionary with the key the picture title and the values the urls
        """
        
        #ar = aspect ratio
        #dimension is in pixels
        
        first = {x['alt_description'] : x['urls']['full'] for x in query_result['results']}
        second = {key : value.replace('entropy','edges') + f'&ar=1:1&fit=crop&w={dimension}' for key, value in first.items()}
        
        return second
    
    def save_pictures(self, url_dict, location):
        """
        Saves the pictures in an url dict

        Parameters
        ----------
        url_dict : Dictionary
            dictionary with the key the picture title and the values the urls
        location : String
            path to location to save file

        Returns
        -------
        None.

        """
        
        for name, url in url_dict.items():
            r = requests.get(url, allow_redirects=True)
            open(f'{name}.jpeg', 'wb').write(r.content)
    
if __name__ == "__main__":
    
    
    
    sp = Spotify()
    playlistId = "4J7qSdpBBzCWO9n3kbQIJg" #Disco playlist with 148 songs    
    df = sp.get_song_df(playlistId)
    query = sp.genre_query(df)
    
    us = Unsplash()
    r = us.query(query)
    q = us.query_to_display_urls(r)
    # us.save_pictures(q, 1)
