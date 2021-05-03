import os

from flask import Flask, request, render_template, session, redirect
from .spotify_api import Spotify
from .unsplash import Unsplash
from . import spotify
from datetime import datetime


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
            playlists = sp.getUserPlaylists(session['user_token'])['items']
        
        print(playlists)
        
        return render_template('playlists.html',
                                   user_display_name=session['user_info']['display_name'],
                                   playlists_data=playlists)
    
    @app.route('/query/<playlistID>')
    def searchImage(playlistID=None):
        
        df = sp.get_song_df(playlistID)
        query = sp.genre_query(df)
        
        images = us.query(query)
        
        
        return render_template('query.html', query=images)
    
    
    
    
        
    app.register_blueprint(spotify.bp)
    
    


    return app