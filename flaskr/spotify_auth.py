import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .startup import getUser, getUserToken

bp = Blueprint('spotify_auth', __name__, url_prefix='/spotify_auth')

@bp.route('/test')
def test():
    return 'hello'

@bp.route('/hello')
def index():
    response = getUser()
    return redirect(response)

@bp.route('/callback')
def joejoe():
    getUserToken(request.args['code'])
    return 'authenticated'