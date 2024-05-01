from flask import Flask, render_template, request, jsonify, session
import os


app = Flask(__name__)
app.secret_key = "secret_key"


def get_image_filenames():
    images_dir = os.path.join(app.static_folder, 'images')
    return [filename for filename in os.listdir(images_dir)]

@app.route('/')
def home():
    # Example image data (replace with your actual image data)
    image_filenames = get_image_filenames()

    # Retrieve poll_data from session, or initialize with zeros if it doesn't exist
    poll_data = session.get('poll_data')
    if poll_data is None:
        poll_data = {image_name: {'yes': 0, 'no': 0} for image_name in image_filenames}
        session['poll_data'] = poll_data
    
    return render_template('index.html', images=image_filenames, poll_data=poll_data)
