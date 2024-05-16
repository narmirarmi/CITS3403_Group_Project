"""
    handle the hashing and accessing of passwords and session tokens
    Werkzeug is a WSGI library that has functions for password hashing
    among other security functions
"""

# begin declarations

import re
from sqlalchemy.exc import IntegrityError

import blueprints
from database.models import db, User, Session

from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

auth = Blueprint('auth', __name__, url_prefix='/auth')

# end declarations

import werkzeug.security as wz
from datetime import datetime, timedelta

# Check the status of the user, i.e. are the currently logged in during their session
@auth.route('/', methods=['POST'])
def check_token():

    session_token = request.form.get('session_token')
    session = validate_session_token(session_token)

    if session is not None:

        user = User.query.get(session.user_id)
        return jsonify(message="Token Received", user=user.username), 200

    return jsonify(message="Invalid Token"), 400


@auth.route('/login', methods=['POST'])
def validateLogin():

    print('endpoint LOGIN_USER reached')
    login_mode = 0  # check if user submitted an email or a username

    #access form data
    email = request.form.get('email')
    password = request.form.get('password')

    errors = []
    if not email:
        errors.append('Email is required')
    if not password:
        errors.append('Password is required')

    # flip login_mode to 1 if email was passed instead of name
    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append('Invalid Email')

    if email and not User.query.filter_by(email=email).first():
        errors.append('Email not found')

    isPasswordValid = check_password(password, User.query.filter_by(email=email).first().password)
    if not isPasswordValid:
        errors.append('Incorrect password')

    if len(errors) != 0:
        return jsonify({"errors": errors}), 400

    # SESSION ID HANDLING
    user = User.query.filter_by(email=email).first()

    for user_sesh in Session.query.filter_by(user_id=user.id):
        db.session.delete(user_sesh)

    new_session = generate_session(user)
    db.session.add(new_session)
    db.session.commit()

    print("Wrote new session ID ", new_session.id)
    # END SESSION ID HANDLING

    return jsonify(message="Successfully logged in as {}".format(user.username), session_token=new_session.id), 200

@auth.route('/register', methods=['POST'])
def register():
    # Access the form data sent with the request
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    errors = []

    # Check required fields
    if not name:
        errors.append('Name is required.')
    if not username:
        errors.append('Username is required.')
    if not email:
        errors.append('Email is required.')
    if not password:
        errors.append('Password is required.')

    if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append('Invalid email format.')

    if password and len(password) < 8:
        errors.append('Password must be at least 8 characters long.')

    # Check for duplicate username / email addresses
    if username and User.query.filter_by(username=username).first():
        errors.append('Username is already taken.')
    ## TEMPORARILY COMMENTED OUT AS SEED WAS GIVING DUPLICATE
    """
    #if email and User.query.filter_by(email=email).first():
    #    errors.append('Email is already in use.')
    """

    if errors:
        return jsonify({"errors": errors}), 400

    # Otherwise, create a new user
    new_user = User(username=username, email=email, password=hash_password(password))
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify(message="Registration failed due to a database error."), 500

    print(f"new user: {new_user.username}")
    return jsonify(message="Registration successful!"), 201

# hash a password
def hash_password(password):
    password_hash = wz.generate_password_hash(password, method="pbkdf2:md5")
    return password_hash

# check a password
def check_password(attempt, password):
    result = wz.check_password_hash(password, attempt)
    return result

# generate new session token based on the current time
def generate_session(user):
    session_hash = wz.generate_password_hash(datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S"))

    new_session = Session(
        id=session_hash,
        session_time=datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S"),
        user_id=user.id
    )
    return new_session

# check if a session token is valid
def validate_session_token(session_token):

    user_session = Session.query.get(session_token)

    if user_session:
        # check four hours ago
        if datetime.strptime(user_session.session_time,"%m/%d/%Y, %H:%M:%S") > datetime.utcnow() - timedelta(hours=current_app.config['SESSION_EXPIRY']):
            return Session.query.get(session_token)
        # if user session has expired, delete it from the table
        else:
            db.session.delete(user_session)
            db.session.commit()
            return None

    return None