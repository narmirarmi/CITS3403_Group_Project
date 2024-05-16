from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os
import re
from database.models import db, Vote, Follow, Comment, User, Image
from database.routes import register_routes


app = Flask(__name__)
app.config.from_object('config.Config')

def create_app(config_filename):

    #init app details
    app.config.from_object(config_filename)
    CORS(app)
    app.secret_key = app.config['SECRET_KEY']

    # init database
    from database.models import db
    db.init_app(app)

    #load blueprints
    from blueprints.auth import auth
    from blueprints.user import user
    app.register_blueprint(auth)
    app.register_blueprint(user)

    return app

register_routes(app, db)

user = None

"""
# get this function to call when the session expires...
def clear_session():
    session.clear()
    return redirect(url_for("login"))

# to persist cookies on the client side, as of the session on the server-side
def set_cookies():
    response = make_response(render_template(...))
    response.set_cookie(key: -, value: -)
    ** to remove cookie instead we set_cooke(key: - , expires=0) # no value
    return response

def get_cookies():
    cookie_value = request.cookies["hashed_password"]
    return ... could potentially add this as a json request when the same user goes to login

"""

# Register the filter using a decorator
@app.template_filter('underscore_to_space')
def underscore_to_space_filter(s):
    return s.replace('_', ' ')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
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


@app.route('/users')
def users():
    with app.app_context():
        # Retrieve all users from the database
        user_list = User.query.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in user_list]
        return jsonify(users=users_data)


if __name__ == "__main__":
    # load from main.cfg
    app = create_app('config.Config')

    #run the application
    app.run(debug=True)