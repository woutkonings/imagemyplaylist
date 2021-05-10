import os

from flask import Flask, request, render_template, session, redirect
from .spotify_api import Spotify
from .unsplash import Unsplash
from . import spotify
from . import playlists
from flaskr.config import Config
import random


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

    @app.route('/test')
    def test():
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
    
    @app.route('/privacy')
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
    @app.route('/test500')
    def test_500():
        return render_template('500.html')

    app.register_blueprint(spotify.bp)
    app.register_blueprint(playlists.bp)
    return app
