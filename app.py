from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    poll_data = {
        'yes': 10,
        'no': 5
    }

    # Example image data (replace with your actual image data)
    images_dir = os.path.join(app.static_folder, 'images')
    image_filenames = [filename for filename in os.listdir(images_dir)]
    return render_template('index.html', images=image_filenames, poll_data=poll_data)

if __name__ == '__main__':
    app.run(debug=True)
