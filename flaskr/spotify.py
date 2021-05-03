import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from .spotify_api import Spotify

bp = Blueprint('spotify', __name__, url_prefix='/spotify')

sp = Spotify()

@bp.route('/auth')
def index():
    response = sp.getUser()
    return redirect(response)

@bp.route('/callback/')
def joejoe():
    sp.getUserToken(request.args['code'])
    session['user_token'] = sp.token_data
    return redirect('/')

@bp.route('/access_token')
def get_access_token():
    return str(sp.getAccessToken())