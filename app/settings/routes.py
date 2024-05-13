import uuid
import os
from flask import Blueprint, flash, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from app.webforms import UpdateForm, User, db
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from app.create_app import create_app

# Create a Blueprint
settings_bp = Blueprint('settings', __name__, template_folder='templates')

bcrypt = Bcrypt()

@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def settings():
    form = UpdateForm()

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about = form.about.data
        
        # Handle profile picture upload
        if form.profile_pic.data:
            profile_pic_filename = save_profile_picture(form.profile_pic.data, create_app())
            current_user.profile_pic = profile_pic_filename
        
        # Check if password is being updated
        if form.new_password.data:
            if bcrypt.check_password_hash(current_user.password, form.current_password.data):
                hashed_password = bcrypt.generate_password_hash(form.new_password.data)
                current_user.password = hashed_password
            else:
                flash('Incorrect current password', 'error')
                return redirect(url_for('settings.settings'))

        db.session.commit()
        flash('Your details have been updated!', 'success')
        return redirect(url_for('settings.settings'))

    # Pre-fill form fields with current user's details
    form.first_name.data = current_user.first_name
    form.last_name.data = current_user.last_name
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.about.data = current_user.about

    return render_template('settings.html', form=form)

def save_profile_picture(profile_pic, app):
    # Get the file extension
    _, file_extension = os.path.splitext(profile_pic.filename)
    # Generate a unique filename using UUID
    profile_pic_name = str(uuid.uuid1()) + file_extension
    # Save the image to the upload folder
    profile_pic.save(os.path.join(app.config['UPLOAD_FOLDER'], profile_pic_name))
    # Return the file path
    return profile_pic_name
