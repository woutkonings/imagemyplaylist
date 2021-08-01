import os
from datetime import timedelta
from flask import Flask, request, render_template, session, redirect
from .spotify_api import Spotify
from .unsplash import Unsplash
from . import spotify
from . import playlists
from flaskr.config import Config
import random
import logging


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='devdevdev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    logging.basicConfig(filename='demo.log', level=logging.DEBUG)
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

    @app.before_first_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)

    @app.get('/')
    def home():
        random_int_0 = random.randint(1,10)
        results = us.query(query='beautiful_nature', page=random_int_0, per_page=30)
        
        images = us.query_to_display_urls(results, dimension=750)
        keys = list(images.keys())
        random_int = random.randint(0,30)


        app.logger.info(images)
        return render_template('home.html', pic_url = images[keys[random_int]])


    @app.get('/about')
    def about():
        return render_template('about.html')

    @app.get('/index')
    def index():
        return render_template('index.html')
    
    @app.get('/session')
    def show_session():
        res = str(session.items())
        return res
    
    @app.get('/privacy')
    def privacy():
        return render_template('privacy.html')
    
    #handle spotify authorisation cancel scenario
    @app.errorhandler(400)
    def auth_error(e):
        return render_template('400.html', scopes=Config.SCOPE), 400
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    app.register_blueprint(spotify.bp)
    app.register_blueprint(playlists.bp)
    
    return app
