# why is this empty

from flask import render_template, request, session

from .models import Image


def register_routes(app, db):
    @app.route('/')
    def index():
        images = Image.query.all()
        image_info = []  # List to store information about each image
        for image in images:
            image_info.append({
                'id': image.id,
                'user_id': image.user_id,
                'image_path': image.image_path,
                'upload_date': image.upload_date.strftime('%Y-%m-%d %H:%M:%S'),  # Format upload date as string
                'votes_count': len(image.votes),  # Get the count of votes for the image
                'comments_count': len(image.comments)  # Get the count of comments for the image
            })
        return render_template('index.html', images=image_info, tab_bottom=True)