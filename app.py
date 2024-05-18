from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from database.models import db, Vote, Follow, Comment, User, Image
from database.routes import register_routes
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('config.Config')
login_manager = LoginManager()
login_manager.init_app(app)

# Function to load a user
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

def create_app(config_filename):

    #init app details
    app.config.from_object(config_filename)
    CORS(app)
    app.secret_key = app.config['SECRET_KEY']

    # init database
    from database.models import db
    db.init_app(app)

    #load blueprints
    from auth.auth import auth
    from user.user import user
    app.register_blueprint(auth)
    app.register_blueprint(user)

    return app

register_routes(app, db)

# Register the filter using a decorator
@app.template_filter('underscore_to_space')
def underscore_to_space_filter(s):
    return s.replace('_', ' ')


if __name__ == "__main__":
    # load from main.cfg
    app = create_app('config.Config')

    #run the application
    app.run(debug=True)