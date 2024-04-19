from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    # Example image data (replace with your actual image data)
    images = [
        {"url": "/static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 1"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 2"},
        {"url": "static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 3"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 4"},
        {"url": "static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 5"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 6"},
        {"url": "static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 7"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 8"},
        {"url": "/static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 1"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 2"},
        {"url": "static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 3"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 4"},
        {"url": "static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 5"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 6"},
        {"url": "static/images/should_i_buy_it_2.png", "alt": "Placeholder Image 7"},
        {"url": "static/images/should_i_buy_it.png", "alt": "Placeholder Image 8"}
    ]
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
