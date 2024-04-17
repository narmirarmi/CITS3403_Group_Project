from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Polling data (yes and no votes)
poll_data = {'yes': 0, 'no': 0}

@app.route('/')
def index():
    return render_template('index.html', poll_data=poll_data)

@app.route('/vote', methods=['POST'])
def vote():
    # Extract the choice from the form data
    choice = request.form['choice']
    
    # Check if the choice is valid and update poll_data
    if choice in poll_data:
        poll_data[choice] += 1
        # Return a JSON response indicating success
        return jsonify({'success': True})
    else:
        # Return a JSON response indicating failure with an error message
        return jsonify({'success': False, 'error': 'Invalid choice'})

@app.route('/results')
def results():
    return jsonify(poll_data)

if __name__ == '__main__':
    app.run(debug=True)
