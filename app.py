from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename
import os
import re
from database.models import db, Vote, Follow, Comment, User, Image


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

    #import views here
    from views.auth import auth
    app.register_blueprint(auth)

    return app

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['IMAGE_EXTENSIONS']

def get_image_filenames():
    images_dir = os.path.join(app.static_folder, 'images')
    return [filename for filename in os.listdir(images_dir)]

# Define the filter function
def underscore_to_space(s):
    return s.replace('_', ' ')

# Register the filter using a decorator
@app.template_filter('underscore_to_space')
def underscore_to_space_filter(s):
    return underscore_to_space(s)

image_filenames = get_image_filenames()

@app.route('/')
def home(banner_message=None):
    image_filenames = get_image_filenames()
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
            filename = filename + "."+extension
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Update poll_data with the new item initialized to 0 counts
            poll_data = session.get('poll_data', {})
            poll_data[filename] = {'yes': 0, 'no': 0}
            session['poll_data'] = poll_data
            
            session['banner_message'] = "Successfully added listing!"
            return redirect(url_for('home'))
        else:
            return "File type not allowed"

    else:
        # Render the form template for GET requests
        return render_template('addListing.html', endpoint='addListing')

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
    # load from main.cfg
    app = create_app('config.Config')

    #run the application
    app.run(debug=True)
