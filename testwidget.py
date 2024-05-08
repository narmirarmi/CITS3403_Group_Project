from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test/WidgetTester.html', widget="poll/PollWidget.html", script="js/LoadPollData.js")

if __name__ == '__main__':
    app.run(debug=True)
