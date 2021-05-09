import os

from flask import Flask, request, render_template, session, redirect
from .spotify_api import Spotify
from .unsplash import Unsplash
from . import spotify
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
        
        #TODO: make this workflow a post method instead of get in order to fix the problem that showall value is not passed in javascript when query is performed.
        
        try:
            searchterm = request_dict.pop('searchterm', None)
            if searchterm != 'none':
                playlists = [x for x in playlists if searchterm in x['name']]
        except:
            'donothing'
            # searchterm = 'none'
            
        try:
            showall = request_dict.pop('showall', None)
            if showall == 'false':
                playlists = [x for x in playlists if len(x['images']) > 1]
        except:
            showall=True
            
        return render_template('playlists.html',
                                   user_display_name=session['user_info']['display_name'],
                                   playlists_data=playlists,
                                   searchterm=searchterm,
                                   showall=showall)

    @app.route('/query/<playlistID>', methods = ['POST', 'GET'])
    def searchImage(playlistID=None):
        
        #TODO: look into different parameters for unsplashed to put into query
        #e.g. make pictures black and white
        
        if request.method == 'POST':
            try:
                searchMethod = request.form['searchMethod']
            except:
                searchMethod = 'genre'
            try:
                searchTerm = request.form['searchTerm']
            except:
                searchTerm = 'none'
        else:
            searchMethod = 'genre'
            searchTerm = 'none'
        
        if searchTerm != 'none' and searchTerm != '':
            images = us.query_to_display_urls(us.query(searchTerm), dimension=750)
        elif searchMethod == 'random':
            num = random.randint(1, 4)
            query = []
            for i in range(num):
                query.append('{KEYWORD}')
            searchTerm = ','.join(query)
            images = us.query_to_display_urls(us.query(searchTerm), dimension=750)
        elif searchMethod in Config.SEARCH_OPTIONS: #make sure to add new 
        #search options to config and to the form option list
            df = sp.get_song_df(playlistID)
            df = df
            searchTerm = eval('sp.' + searchMethod +'_query(df)')
            images = us.query_to_display_urls(us.query(searchTerm), dimension=750)
        
        print('searchTerm ' + searchTerm, flush=True)
        print('searchMethod ' + searchMethod, flush=True)
        print('images ' + str(images.keys()), flush=True)
        
        
        return render_template('query.html', 
                               user_display_name=session['user_info']['display_name'],
                               images=images, 
                               playlistID=playlistID)
    
    @app.route('/setimage')
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
            return redirect('/playlists')
        elif res.status_code == 413 and res.reason == 'Request Entity Too Large':
            #decrease the square with 50 pixels until request is accepted
            prevDimension = imageUrl.split('w=')[-1]
            print('prev = ' + prevDimension, flush=True)
            newDimension = str(int(prevDimension) - 50)
            print('dim = ' + newDimension, flush=True)
            newImageUrl = imageUrl.replace('w=' + prevDimension, 'w=' + newDimension)
            return redirect(f"/setimage?playlistID={playlistID}&imageUrl={newImageUrl}")
        else:
            return redirect('/playlists')
    
    
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

    return app
