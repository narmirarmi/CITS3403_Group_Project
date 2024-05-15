import sqlite3
from flask import jsonify, request
from flask_login import current_user
from .models import Follow

def register_routes(app, db):
    @app.route('/', methods=['GET', 'POST'])
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

    def follow_user(current_user_id, user_id):
        conn = sqlite3.connect('your_database.db')
        c = conn.cursor()
        c.execute("INSERT INTO follow (follower_id, followee_id) VALUES (?, ?)", (current_user_id, user_id))
        conn.commit()
        conn.close()

    def unfollow_user(current_user_id, user_id):
        conn = sqlite3.connect('your_database.db')
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
