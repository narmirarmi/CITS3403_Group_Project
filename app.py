from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os
import re
from database.models import db, Vote, Follow, Comment, User, Image


app = Flask(__name__)
CORS(app)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///should_i_buy_it.db'
db.init_app(app)

from database.routes import register_routes
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

def get_image_filenames():
    images_dir = os.path.join(app.static_folder, 'images')
    return [filename for filename in os.listdir(images_dir)]

image_filenames = get_image_filenames()

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginuser', methods=['POST'])
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

    if errors:
        return jsonify({"errors": errors}), 400

    return jsonify(message="Successfully logged in as {}".format(user)), 201

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
    app.run(debug=True)
