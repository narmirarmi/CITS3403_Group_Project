from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os
import re
from database.models import db, Vote, Follow, Comment, User, Image


app = Flask(__name__)
CORS(app)
app.secret_key = "secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///should_i_buy_it.db'
app.config['UPLOAD_FOLDER'] = "static\images"
db.init_app(app)

# Define the allowed file extensions
IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in IMAGE_EXTENSIONS

def get_image_filenames():
    images_dir = os.path.join(app.static_folder, 'images')
    return [filename for filename in os.listdir(images_dir)]

image_filenames = get_image_filenames()

@app.route('/')
def home(banner_message=None):
    # Retrieve poll_data from session, or initialize with zeros if it doesn't exist
    poll_data = session.get('poll_data')
    print(poll_data)
    if poll_data is None:
        poll_data = {image_name: {'yes': 0, 'no': 0} for image_name in image_filenames}
        session['poll_data'] = poll_data

    banner_message = session.pop('banner_message', None)  # Retrieve and remove banner_message from session

    return render_template('index.html', images=image_filenames, poll_data=poll_data, tab_bottom=True, banner_message=banner_message)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/post', methods=['GET', 'POST'])
def addListing():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image = request.files['image']
        # Handle the form submission
        print(title)
        print(description)
        print(image)

        # Check if file is uploaded
        if image.filename == '':
            return "No file selected"
        # Check if file has an allowed extension
        if image and allowed_file(image.filename):
            # Saves to the images file, and prevent SQL injection and other attacks of that type
            filename = secure_filename(title)
            extension = image.filename.split(".")[-1]
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename + extension))
            session['banner_message'] = "Successfully added listing!"
            return redirect(url_for('home'))
        else:
            return "File type not allowed"

    else:
        # Render the form template for GET requests
        return render_template('addListing.html', endpoint='addListing')


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
