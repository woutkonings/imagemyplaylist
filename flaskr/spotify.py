import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from .spotify_api import Spotify

bp = Blueprint('spotify', __name__, url_prefix='/spotify')

st = Spotify()

@bp.route('/auth')
def index():
    response = st.getUser()
    return redirect(response)

@bp.route('/callback/')
def joejoe():
    st.getUserToken(request.args['code'])
    return redirect('/')

@bp.route('/access_token')
def get_access_token():
    return str(st.getAccessToken())