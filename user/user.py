"""
    Handle profile accessing and rerouting on login condition
"""

from sqlalchemy.exc import IntegrityError
from database.models import db, User, Session
from jinja2 import TemplateNotFound
from database.routes import get_followers_count, get_following_count
from flask_login import current_user

from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)

import database.routes

user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

@user.route('/')
def redirect_to_user():
    return redirect(url_for('user.showUser', userid=current_user.id))

@user.route('/<userid>')
def showUser(userid):

    try:
        return render_template('user.html',
                               user=User.query.get(userid),
                               followers=get_followers_count(userid),
                               following=get_following_count(userid))
    except TemplateNotFound:
        abort(404)