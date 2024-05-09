"""
    handle the hashing and accessing of passwords and session tokens
    Werkzeug is a WSGI library that has functions for password hashing
    among other security functions
"""

# begin declarations

import functools
import re
from sqlalchemy.exc import IntegrityError
from database.models import db, User

from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)

auth = Blueprint('auth', __name__, url_prefix='/auth')

# end declarations

import werkzeug.security as wz
from datetime import datetime

@auth.route('/login', methods=['POST'])
def validateLogin():

    print('endpoint LOGIN_USER reached')
    login_mode = 0  # check if user submitted an email or a username

    #access form data
    user = request.form.get('username')
    password = request.form.get('password')

    errors = []
    if not user:
        errors.append('Username / Email is required.')
    if not password:
        errors.append('Password is required.')

    # flip login_mode to 1 if email was passed instead of name
    if user and re.match(r"[^@]+@[^@]+\.[^@]+", user):
        login_mode = 1

    # check password against email if login_mode is 1
    if login_mode == 1:
        if user and not User.query.filter_by(email=user).first():
            errors.append('Email not found')
        elif user and password != User.query.filter_by(email=user).first().password:
            errors.append('Incorrect password')

    # check password against username if login_mode is 0
    elif login_mode == 0:
        if user and not User.query.filter_by(username=user).first():
            errors.append('Username not found')
        elif user and password != User.query.filter_by(username=user).first().password:
            errors.append('Incorrect password')

    if len(errors) != 0:
        return jsonify({"errors": errors}), 400

    # SESSION ID HANDLING
    return jsonify(message="Successfully logged in as {}".format(user)), 200

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
    new_user = User(username=username, email=email, password=password)
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
    bytes = password.encode('utf-8')
    password_hash = wz.generate_password_hash(password, method="pbkdf2:md5")
    return password_hash

# check a password
def check_password(attempt, password):
    attemptBytes = attempt.encode('utf-8')
    result = wz.check_password_hash(attemptBytes, password)
    return result

# generate new session token based on the current time
def generate_session_token():
    bytes = datetime.now().encode('utf-8')
    session_hash = wz.generate_password_hash(bytes)
    return session_hash

# check if a session token is valid
def check_session_token(attempt, session_token):
    attemptBytes = attempt.encode('utf-8')
    result = wz.check_password_hash().checkpw(attemptBytes, session_token)
    return result