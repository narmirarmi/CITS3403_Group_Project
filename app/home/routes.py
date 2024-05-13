from flask import Blueprint, redirect, render_template, url_for, current_app
from flask_login import current_user, login_required
from app.webforms import Image, ImageForm, db
from werkzeug.utils import secure_filename
import os

# Create a Blueprint
home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    all_images = Image.query.all()
    # Render the index.html template and pass the images to it
    return render_template('index.html', all_images=all_images)
