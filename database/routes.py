import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, flash
from flask_login import current_user
from .models import Follow, Image, Vote
import os
from datetime import datetime
from werkzeug.utils import secure_filename

def follow_user(current_user_id, user_id):
    conn = sqlite3.connect('should_i_buy_it.db')
    c = conn.cursor()
    c.execute("INSERT INTO follow (follower_id, followee_id) VALUES (?, ?)", (current_user_id, user_id))
    conn.commit()
    conn.close()

def unfollow_user(current_user_id, user_id):
    conn = sqlite3.connect('should_i_buy_it.db')
    c = conn.cursor()
    c.execute("DELETE FROM follow WHERE follower_id = ? AND followee_id = ?", (current_user_id, user_id))
    conn.commit()
    conn.close()


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
    def index():
        banner_message = flash('success')
        print(banner_message)

        images = Image.query.all()
        image_info = []  # List to store information about each image
        for image in images:
            likes_count = Vote.query.filter_by(image_id=image.id, type='like').count()
            dislikes_count = Vote.query.filter_by(image_id=image.id, type='dislike').count()

            user_vote = None  # Default to None if user hasn't voted
            #if current_user.is_authenticated:  # Check if user is authenticated 
            #replace with the current_user
            user_vote = Vote.query.filter_by(image_id=image.id, user_id=2).first()
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
        return render_template('index.html', images=image_info, tab_bottom=True, banner_message=banner_message)
    
    @app.route('/vote', methods=['POST'])
    def vote():
            selected_image = request.form['image']
            user_id = 1#current_user.get_id() # THIS NEEDS IS FROM THE SESSION
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
                current_user = 1
                # Update poll_data with the new item initialized to 0 counts
                new_image = Image(user_id=current_user, image_path=filename, post_title=title, post_description=description, upload_date=datetime.utcnow())
                db.session.add(new_image)
                db.session.commit()
                flash('Listing added successfully', 'success')
                return redirect(url_for('index'))
            else:
                return "File type not allowed"

        else:
            # Render the form template for GET requests
            return render_template('addListing.html', endpoint='addListing')
        
        