from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_cors import CORS
from database.models import db, Vote, Follow, Comment, User, Image
from database.routes import register_routes
from flask_login import LoginManager
from config import Config, DevelopmentConfig, TestingConfig, InitialisingConfig


def create_app(config_class='config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)
    app.secret_key = app.config['SECRET_KEY']

    from database.models import db
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from database.models import User
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        from flask import redirect, url_for
        return redirect(url_for('login'))

    from blueprints.auth import auth
    from blueprints.user import user
    app.register_blueprint(auth)
    app.register_blueprint(user)

    from database.routes import register_routes
    register_routes(app, db)

    @app.template_filter('underscore_to_space')
    def underscore_to_space_filter(s):
        return s.replace('_', ' ')

    return app


if __name__ == "__main__":
    import os
    env_config = {
        'development': 'config.DevelopmentConfig',
        'testing': 'config.TestingConfig',
        'production': 'config.ProductionConfig'
    }
    # Determine the configuration based on the FLASK_ENV environment variable
    config_class = env_config.get(os.getenv('FLASK_ENV', 'development'), 'config.DevelopmentConfig')
    app = create_app(config_class)
    app.run(debug=True)