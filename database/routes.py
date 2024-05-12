# why is this empty

from flask import render_template, request, session

from .models import Image


def register_routes(app, db):
    @app.route('/')
    def index():
        poll_data = session.get('poll_data')
        session['poll_data'] = poll_data
        image = Image.query.all()
        images = [i.image_path for i in image]  # Extract image paths 
        return render_template('index.html', images=images, poll_data=poll_data, tab_bottom=True)