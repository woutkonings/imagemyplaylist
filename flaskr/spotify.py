import functools
from .helper import determine_host
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from .spotify_api import Spotify
import flaskr

bp = Blueprint('spotify', __name__, url_prefix='/spotify')

sp = Spotify()

@bp.route('/auth')
def auth():
    callback_url = determine_host(request.headers)
    response = sp.getUser(callback_url)
    return redirect(response)

@bp.route('/callback/')
def joejoe():
    callback_url = determine_host(request.headers)
    sp.getUserToken(code=request.args['code'], callback_url=callback_url)
    session['user_token'] = sp.token_data[0]
    print('user_token')
    print(session['user_token'])
    session['user_info'] = sp.getUserInfo(session['user_token'])
    return redirect('/')
    # return redirect(url_for('home'))

@bp.route('/access_token')
def get_access_token():
    return str(sp.getAccessToken())

