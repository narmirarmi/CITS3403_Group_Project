from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required, logout_user
from flask_bcrypt import Bcrypt

# Create a Blueprint
logout_bp = Blueprint('logout', __name__, template_folder='templates')

bcrypt = Bcrypt()

@logout_bp.route('/', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')  # Flash message
    return redirect(url_for('login.login'))