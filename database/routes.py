# why is this empty

from flask import render_template, request, session, jsonify
from flask_login import current_user

from .models import Image, Vote

def register_routes(app, db):
    @app.route('/')
    def index():
        images = Image.query.all()
        image_info = []  # List to store information about each image
        for image in images:
            likes_count = Vote.query.filter_by(image_id=image.id, type='like').count()
            dislikes_count = Vote.query.filter_by(image_id=image.id, type='dislike').count()
            
            image_info.append({
                'id': image.id,
                'user_id': image.user_id,
                'image_path': image.image_path,
                'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
                'likes_count': likes_count,
                'dislikes_count': dislikes_count,
                'comments_count': len(image.comments)
            })
        return render_template('index.html', images=image_info, tab_bottom=True)
    
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