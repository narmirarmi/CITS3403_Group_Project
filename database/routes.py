import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, Blueprint
from flask_login import current_user, login_required, LoginManager
from .models import db, Follow, Image, Vote, User
from sqlalchemy.exc import IntegrityError
import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename

#Needs to be globally accessible
image_info = []

def follow_user(current_user_id, user_id):
    db.session.add(Follow(followee_id=user_id, follower_id=current_user_id))
    db.session.commit()

def unfollow_user(current_user_id, user_id):
    db.session.delete(Follow.query.filter_by(followee_id=user_id, follower_id=current_user_id).first())
    db.session.commit()

def isFollowing(current_user_id, followed_user_id):
    if Follow.query.filter_by(follower_id=current_user_id, followee_id=followed_user_id).first() is not None:
        return True
    return False

def get_followers_count(user_id):
    followers_count = Follow.query.filter_by(followee_id=user_id).count()
    return followers_count

def get_following_count(user_id):
    following_count = Follow.query.filter_by(follower_id=user_id).count()
    return following_count

# Function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'jpeg', 'png', 'gif']

def register_routes(app, db):

    @app.route('/')
    @app.route('/index')
    @login_required
    def index():

        images = Image.query.all()
        for image in images:
            likes_count = Vote.query.filter_by(image_id=image.id, type='like').count()
            dislikes_count = Vote.query.filter_by(image_id=image.id, type='dislike').count()

            user_vote = None  # Default to None if user hasn't voted
            #if current_user.is_authenticated:  # Check if user is authenticated 
            #replace with the current_user
            user_vote = Vote.query.filter_by(image_id=image.id, user_id=current_user.id).first()
            if user_vote:
                print(user_vote.type)
                user_vote = user_vote.type  # Get the vote type if user has voted
        
            
            image_info.append({
                'id': image.id,
                'user_id': image.user_id,
                'image_path': image.image_path,
                'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                'likes_count': likes_count,
                'dislikes_count': dislikes_count,
                'comments_count': len(image.comments),
                'user_vote': user_vote,
                'image_title': image.post_title,
                'image_description': image.post_description
            })
        print("Current user", current_user.username)
        return render_template('index.html', images=image_info, tab_bottom=True)
    
    @app.route('/profile')
    @login_required
    def profile():
        # Aggregate counts
        num_followers = Follow.query.filter_by(followee_id=current_user.id).count()
        num_following = Follow.query.filter_by(follower_id=current_user.id).count()
        num_posts = Image.query.filter_by(user_id=current_user.id).count()
        num_likes = db.session.query(Vote).join(Image).filter(
            Vote.type == 'like',
            Image.user_id == current_user.id
        ).count()

        return render_template('user.html', 
                            followers=num_followers, 
                            following=num_following,
                            num_posts=num_posts, 
                            num_likes=num_likes, tab_bottom=True)

    
    @app.route('/vote', methods=['POST'])
    @login_required
    def vote():
            selected_image = request.form['image']
            user_id = current_user.id
            vote_type = request.form['choice']

            #This is the case where they are not logged in
            if user_id is None:
                return jsonify({'error': 'User not logged in'}), 401

            if "/images" in selected_image:
                selected_image = selected_image.split("/images/")[1]
            #Vote references ID not path, so needs to get the corresponding ID
            image_id = db.session.query(Image.id).filter_by(image_path=selected_image).first()
            # Needs to be the first item image_id the tuple
            image_id = image_id[0]

            # Check if they already voted for this image
            existing_vote = Vote.query.filter_by(image_id=image_id, user_id=user_id).first()
            if existing_vote:
                # If the user has already voted, may change like to dislike
                existing_vote.type = vote_type
                print(existing_vote.type)
            else:
                # If the user hasn't voted yet, create a new vote record
                new_vote = Vote(image_id=image_id, user_id=user_id, type=vote_type)
                db.session.add(new_vote)

            db.session.commit()
            print(image_id)
            # Get the count of likes and dislikes for the selected image and user
            likes_count = Vote.query.filter_by(image_id=image_id, type='like').count()
            dislikes_count = Vote.query.filter_by(image_id=image_id, type='dislike').count()
            print(likes_count)
            print(dislikes_count)
            # Respond with success message or updated vote count
            return jsonify({'message': 'Vote recorded successfully', 'likes_count': likes_count, 'dislikes_count': dislikes_count, 'vote_type': vote_type})
    @app.route('/follow', methods=['GET', 'POST'])
    @login_required
    def follow():
        if request.method == 'POST':
            user_id = request.form.get('user_id')  # ID of the user to follow or unfollow
            action = request.form.get('action')    # Action: 'follow' or 'unfollow'
            current_user_id = 1  # current_user.get_id()

            if action == 'follow':
                follow_user(current_user_id, user_id)
            elif action == 'unfollow':
                unfollow_user(current_user_id, user_id)
            else:
                return jsonify(error="Invalid action")
            
            follower = get_followers_count(current_user_id)
            following = get_following_count(current_user_id)

            return jsonify({'message': 'Follow recorded successfully', 'follower': follower, 'following': following, 'action': action})
    
    @app.route('/post', methods=['POST'])
    @login_required
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
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                current_user = 1
                # Update poll_data with the new item initialized to 0 counts
                new_image = Image(user_id=current_user, image_path=filename, post_title=title, post_description=description, upload_date=datetime.utcnow())
                db.session.add(new_image)
                db.session.commit()
                return render_template('index.html', images=image_info, tab_bottom=True, banner_message=f"Listing {title} added successfully!")
            else:
                return "File type not allowed"
            
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