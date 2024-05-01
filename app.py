from flask import Flask, render_template, request, jsonify, session
import os


app = Flask(__name__)
app.secret_key = "secret_key"


def get_image_filenames():
    images_dir = os.path.join(app.static_folder, 'images')
    return [filename for filename in os.listdir(images_dir)]

@app.route('/')
def home():
    image_filenames = get_image_filenames()
    
    for filename in image_filenames:
        """ THIS NEEDS TO BE RETRIEVED DYNAMICALLY FROM DATABASE NOT JUST SET TO 0 """

    # Retrieve poll_data from session, or initialize with zeros if it doesn't exist
    poll_data = session.get('poll_data')
    print(poll_data)
    if poll_data is None:
        poll_data = {image_name: {'yes': 0, 'no': 0} for image_name in image_filenames}
        session['poll_data'] = poll_data
        print(poll_data)
    
    return render_template('index.html', images=image_filenames, poll_data=poll_data)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        #Do not want the whole extended path
        selected_candidate = request.form['image'].split("/")[-1]
        print(selected_candidate)
        yesVote = request.form['choice'] == "yes"
        print(request.form['choice'])
        votes = session.get('poll_data')
        if yesVote:
            votes[selected_candidate]["yes"] += 1
        else:
            votes[selected_candidate]["no"] += 1

        session['poll_data'] = votes

    return home()



if __name__ == "__main__":
    app.run(debug=True)
