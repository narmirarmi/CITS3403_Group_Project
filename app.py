from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Example image data (replace with your actual image data)
    images_dir = os.path.join(app.static_folder, 'images')
    image_filenames = [filename for filename in os.listdir(images_dir)]

    # Initialize poll data for each image ***IN THE FUTURE THIS WILL BE READ FROM DB****
    poll_data = {image_name: {'yes': 0, 'no': 0} for image_name in image_filenames}

    return render_template('index.html', images=image_filenames, poll_data=poll_data)

@app.route('/vote', methods=['POST'])
def vote():
    # Receive form data
    choice = request.form['choice']
    print(choice)
    print(request.form['image_name'])
    
    # Process the vote (update poll data, etc.)
    
    # Return a response (e.g., indicating success)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
