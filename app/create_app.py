import os
from flask import Flask
from flask_login import LoginManager
from app.webforms import db, User
from app.routes import configure_routes

def create_app():
    app = Flask(__name__, static_folder='static')
    
    # Configuration settings
    app.config['SECRET_KEY'] = '2fe112ef6f5d5d9b9e9eb4943024846d'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/upload_folder')

    # Configure database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login.login"  # Update the login view name

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints with unique names and prefixes
    from app.login import login_bp
    from app.logout import logout_bp
    from app.register import register_bp
    from app.settings import settings_bp
    from app.profile import profile_bp
    from app.home import home_bp

    app.register_blueprint(login_bp, url_prefix='/login')
    app.register_blueprint(logout_bp, url_prefix='/logout')
    app.register_blueprint(register_bp, url_prefix='/register')
    app.register_blueprint(settings_bp, url_prefix='/settings')
    app.register_blueprint(profile_bp, url_prefix='/profile')
    app.register_blueprint(home_bp, url_prefix='/home')

    # Configure routes
    configure_routes(app)

    # Create database and tables
    with app.app_context():
        db.create_all()

    return app
