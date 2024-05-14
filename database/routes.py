# why is this empty

from flask import render_template, request, session

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