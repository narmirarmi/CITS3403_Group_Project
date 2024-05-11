from flask import Flask, render_template, request, jsonify, session
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

    return render_template('index.html', images=image_filenames, poll_data=poll_data, tab_bottom=True)


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
    
@app.route('/vote', methods=['POST'])
def vote():
    #Do not want the whole extended path
    selected_candidate = request.form['image'].split("/")[-1]
    yesVote = request.form['choice'] == "yes"
    votes = session.get('poll_data')
    if yesVote:
        votes[selected_candidate]["yes"] += 1
    else:
        votes[selected_candidate]["no"] += 1

    session['poll_data'] = votes
    print(jsonify(votes))
    return jsonify(votes)  # Respond with poll data as JSON



if __name__ == "__main__":
    app.run(debug=True)
