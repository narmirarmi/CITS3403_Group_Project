from flask import Flask, Blueprint, render_template, redirect, url_for
from flask_login import login_user, LoginManager
from app.webforms import LoginForm, User
from flask_bcrypt import Bcrypt

# Create a Blueprint
login_bp = Blueprint('login', __name__, template_folder='templates')

bcrypt = Bcrypt()
login_manager = LoginManager()

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home.home'))
    return render_template('login.html', form=form)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login.login'))

@login_bp.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html')

def init_app(app):
    app.register_blueprint(login_bp)
    bcrypt.init_app(app)
    login_manager.init_app(app)