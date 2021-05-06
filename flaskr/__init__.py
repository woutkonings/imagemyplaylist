import os

from flask import Flask, request, render_template, session, redirect, jsonify
from .spotify_api import Spotify
from .unsplash import Unsplash
from . import spotify
from datetime import datetime
from flaskr.config import Config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='devdevdev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    
    sp = Spotify()
    us = Unsplash()

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        # now = datetime.now()
        # t = now.strftime("%H:%M:%S")
        # session['visit_time'] =  str(t)
        dict_headers = dict(request.headers)
        for key in dict_headers:
            print(key + ': ' + dict_headers[key])
        return render_template('home.html')

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/index')
    def index():
        return render_template('index.html')
    
    @app.route('/session')
    def show_session():
        res = str(session.items())
        return res

    @app.route('/playlists')
    def playlists():
        
        if session.get('user_token') is None: #check if authentication already done
            return redirect('/spotify/auth')
        else: 
            playlists = sp.getUserPlaylists(session['user_token'])
            
        request_dict = request.args.copy()
        
        try:
            searchterm = request_dict.pop('searchterm', None)
            playlists = [x for x in playlists if searchterm in x['name']]
        except:
            searchterm = 'none'
            
        try:
            showall = request_dict.pop('showall', None)
            if not showall == 'true':
                playlists = [x for x in playlists if len(x['images']) > 1]
        except:
            showall=True
            
        return render_template('playlists.html',
                                   user_display_name=session['user_info']['display_name'],
                                   playlists_data=playlists,
                                   showall=showall)
    
    # @app.route('/searchplaylists')
    # def searchplaylists():
    #     try:
    #         searchterm = request.args.get('searchterm', 0, type=str)
    #         playlists = sp.getUserPlaylists(session['user_token'])
    #         playlists_data = [x for x in playlists if searchterm in x['name']]
    #         playlists_data_return = jsonify(updated=True,
    #                                         playlists_data=playlists_data)
    #         return playlists_data_return
    #     except Exception as e:
    #         return str(e)
    
    

    @app.route('/query/<playlistID>')
    def searchImage(playlistID=None):
        
        df = sp.get_song_df(playlistID)
        query = sp.genre_query(df)
        
        result = us.query(query)
        images = us.query_to_display_urls(result, size = 'thumb')
        
        return render_template('query.html', query=images, playlistID=playlistID)
    
    @app.route('/setimage')
    def setImage(playlistID=None):
        
        request_dict = request.args.copy()
        
        playlistID  = request_dict.pop('playlistID', None)
        imageUrl  = request_dict.pop('imageUrl', None)
        for key in request_dict.keys():
            imageUrl = imageUrl + "&" + key + "=" + request_dict.get(key)
        
        res = sp.set_playlist_image(playlistID, imageUrl, session['user_token'])
        
        return redirect('/playlists')

    app.register_blueprint(spotify.bp)

    return app
