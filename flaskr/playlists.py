from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from .spotify_api import Spotify
from .config import Config
from .unsplash import Unsplash
import random
import os

sp = Spotify()
us = Unsplash()
bp = Blueprint('playlists', __name__, url_prefix='/playlists')

@bp.route('/display')
def display_playlists():
    if session.get('user_token') is None: #check if authentication already done
        return redirect('/spotify/auth')
    else: 
        playlists = sp.getUserPlaylists(session['user_token'])
    request_dict = request.args.copy()
    #TODO: make this workflow a post method instead of get in order to fix the problem that showall value is not passed in javascript when query is performed.
    try:
        searchterm = request_dict.pop('searchterm', None)
        if searchterm != 'none':
            playlists = [x for x in playlists if searchterm in x['name']]
    except:
        pass
        
    try:
        showall = request_dict.pop('showall', None)
        if showall == 'false':
            playlists = [x for x in playlists if len(x['images']) > 1]
    except:
        showall=True
    no_of_playlists = len(playlists)
    return render_template('playlists.html',
                            user_display_name=session['user_info']['display_name'],
                            playlists_data=playlists,
                            searchterm=searchterm,
                            showall=showall,
                            no_of_playlists=no_of_playlists)


@bp.route('/query/<playlistID>', methods = ['POST', 'GET'])
def searchImages(playlistID=None):

    #TODO: look into different parameters for unsplashed to put into query
    #e.g. make pictures black and white
    print(os.getcwd())
    if request.method == 'POST':
        try:
            searchMethod = request.form['searchMethod']
            print(searchMethod)
        except:
            searchMethod = 'genre'
        try:
            searchTerm = request.form['searchTerm']
        except:
            searchTerm = 'none'
    else:
        searchMethod = 'random'
        searchTerm = 'none'
    if searchTerm != 'none' and searchTerm != '':
        query_results = us.query(query=searchTerm, per_page=30)
        images = us.query_to_display_urls(query_results, dimension=750)
    elif searchMethod == 'random':
        with open(os.path.join(os.getcwd(), 'flaskr/files/adjectives.txt'), 'r') as file:
            lines = file.readlines()
            no_of_words = 3
            query = []
            for i in range(no_of_words):
                random_num = random.randint(0, len(lines))
                query.append(lines[random_num].replace(' ','').strip())
            searchTerm = ', '.join(query)
            query_results = us.query(query=searchTerm, per_page=30)
            images = us.query_to_display_urls(query_results, dimension=750)
    elif searchMethod in Config.SEARCH_OPTIONS: #make sure to add new 
    #search options to config and to the form option list
        if session.get('user_token') is None: #check if authentication already done
            return redirect('/spotify/auth')
        df = sp.get_song_df(playlistID, token=session.get('user_token'))
        df = df
        searchTerm = eval('sp.' + searchMethod +'_query(df)')
        query_results = us.query(query=searchTerm, per_page=30)
        images = us.query_to_display_urls(query_results, dimension=750)
    print('searchTerm ' + searchTerm, flush=True)
    print('searchMethod ' + searchMethod, flush=True)
    print('images ' + str(images.keys()), flush=True)
    if session.get('user_token') is None: #check if authentication already done
        return redirect('/spotify/auth')
    else: 
        playlist_dict = sp.get_playlist(playlist_id=playlistID, token=session['user_token'])
    playlist_name = playlist_dict['name']
    return render_template('query.html', 
                            user_display_name=session['user_info']['display_name'],
                            images=images, 
                            playlistID=playlistID,
                            playlist_name=playlist_name,
                            searchMethod=searchMethod,
                            searchTerm=searchTerm,
                            playlist_dict=playlist_dict)


@bp.route('/setimage')
def setImage(playlistID=None):
    request_dict = request.args.copy()
    
    playlistID  = request_dict.pop('playlistID', None)
    imageUrl  = request_dict.pop('imageUrl', None)
    for key in request_dict.keys():
        imageUrl = imageUrl + "&" + key + "=" + request_dict.get(key)
    res = sp.set_playlist_image(playlistID, imageUrl, session['user_token'])
    print(res.status_code, flush=True)
    print(res.reason, flush=True)
    if res.status_code == 202:
        #if accepted return to playlists
        return redirect(f'/playlists/query/{playlistID}')

        
    elif res.status_code == 413 and res.reason == 'Request Entity Too Large':
        #decrease the square with 50 pixels until request is accepted
        prevDimension = imageUrl.split('w=')[-1]
        print('prev = ' + prevDimension, flush=True)
        newDimension = str(int(prevDimension) - 50)
        print('dim = ' + newDimension, flush=True)
        newImageUrl = imageUrl.replace('w=' + prevDimension, 'w=' + newDimension)
        return redirect(f"/setimage?playlistID={playlistID}&imageUrl={newImageUrl}")
    else:
        return redirect(f'/playlists/query/{playlistID}')
