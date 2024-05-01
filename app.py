from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import os
from database import routes


app = Flask(__name__)
CORS(app)
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



@app.route('/register', methods=['POST'])
def register():
    # Access the form data sent with the request
    name = request.form.get('name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # add validation here

    # add processing to initialise a new user here, e.g. database entry, etc.


    # Print received data
    print("Registration data received:")
    print(f"Name: {name}")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")

    # Temporarily, return a simple response
    return jsonify(message="Registration data received"), 200


if __name__ == "__main__":
    app.run(debug=True)