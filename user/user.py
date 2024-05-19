"""
    Handle profile accessing and rerouting on login condition
"""

from sqlalchemy.exc import IntegrityError
from database.models import db, User, Session
from jinja2 import TemplateNotFound
from database.routes import get_followers_count, get_following_count, isFollowing, unfollow_user, follow_user, get_posts
from flask_login import current_user

from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)

import database.routes

user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

@user.route('/')
def redirect_to_user():
    if current_user.is_active:
        return redirect(url_for('user.showUser', userid=current_user.id))
    else:
        return redirect(url_for('login'))

@user.route('/<userid>')
def showUser(userid):

    try:
        return render_template('user.html',
                               user=User.query.get(userid),
                               isFollowing=isFollowing(current_user.id, userid),
                               followers=get_followers_count(userid),
                               following=get_following_count(userid),
                               posts=get_posts(userid))
    except TemplateNotFound:
        abort(404)

@user.route('/follow', methods=['POST'])
def followUser():
    followee = request.form.get('userid')
    print("retrieved followee id of ", followee)

    if isFollowing(current_user.id, followee):
        unfollow_user(current_user.id, followee)
        return jsonify(message='Successfully unfollowed {}'.format(followee),
                       status="unfollowed",
                       follower_count=get_followers_count(followee),
                       following_count=get_following_count(followee)), 200
    else:
        follow_user(current_user.id, followee)
        return jsonify(message='Successfully followed {}'.format(followee),
                       status="followed",
                       follower_count=get_followers_count(followee),
                       following_count=get_following_count(followee)), 200

    return jsonify('User does not exist'), 400

