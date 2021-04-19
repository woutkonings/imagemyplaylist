import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from .startup import getUser, getUserToken, getAccessToken

bp = Blueprint('spotify', __name__, url_prefix='/spotify')

@bp.route('/auth')
def index():
    response = getUser()
    return redirect(response)

@bp.route('/callback/')
def joejoe():
    getUserToken(request.args['code'])
    return redirect(url_for('hello'))

@bp.route('/access_token')
def get_access_token():
    return str(getAccessToken())