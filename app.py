from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
import os
import re
from database.models import db, User
import functools


app = Flask(__name__)

# app factory
def create_app(config_filename):

    #init app details
    app.config.from_object(config_filename)
    CORS(app)
    app.secret_key = app.config['SECRET_KEY']

    # init database
    from database.models import db
    db.init_app(app)

    #import views here
    from views.auth import auth
    app.register_blueprint(auth)

    return app


def get_image_filenames():
    images_dir = os.path.join(app.static_folder, 'images')
    return [filename for filename in os.listdir(images_dir)]


image_filenames = get_image_filenames()


@app.route('/')
def home():
    # Retrieve poll_data from session, or initialize with zeros if it doesn't exist
    poll_data = session.get('poll_data')
    print(poll_data)
    if poll_data is None:
        poll_data = {image_name: {'yes': 0, 'no': 0} for image_name in image_filenames}
        session['poll_data'] = poll_data
    return render_template('index.html', images=image_filenames, poll_data=poll_data)


@app.route('/login')
def login():
    return render_template('login.html')


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
