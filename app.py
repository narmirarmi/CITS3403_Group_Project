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


@app.route('/vote', methods=['POST'])
def vote():
    # Receive form data
    choice = request.form['choice']
    name = request.form['image']
    print(name)
    
    # Retrieve poll_data from session
    poll_data = session.get('poll_data', {})
    
    # Update poll_data
    if choice == "yes":
        poll_data[name]['yes'] += 1
    elif choice == "no":
        poll_data[name]['no'] += 1
    
    # Store updated poll_data back in session
    session['poll_data'] = poll_data
    
    # Return a response (e.g., indicating success)
    return home()

@app.route('/profile', methods=["GET"])
def profile():
    # Your profile route logic here
    return render_template('profile.html')
if __name__ == '__main__':
    app.run(debug=True)
