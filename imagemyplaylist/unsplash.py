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


if __name__ == "__main__":
    
    
    unsplash_client_id = config.UNSPLASH_CLIENT_ID
    unsplash_client_secret = config.UNSPLASH_CLIENT_SECRET
    
    
    headers = {
    "Authorization": "Client-ID " + unsplash_client_id
    }
    
    req_url = 'https://api.unsplash.com/search/photos?page=1&query=office'
    res = requests.get(url=req_url, headers=headers)
    r = res.json()