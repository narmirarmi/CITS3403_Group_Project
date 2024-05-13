from flask import Blueprint, redirect, render_template, url_for, current_app
from flask_login import current_user, login_required
from app.webforms import Image, ImageForm, db
from werkzeug.utils import secure_filename
import os

# Create a Blueprint
profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def profile():
    form = ImageForm()
    print("form")
    if form.validate_on_submit():
        print("Form validation passed")

        file = form.image_path.data
        print("File:", file)
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        new_image = Image(user_id=current_user.user_id, image_path=filename)
        db.session.add(new_image)
        db.session.commit()

        # Redirect to the profile page after uploading the photo
        return redirect(url_for('profile.profile'))
    else:
        print("Form validation failed")
        print(form.errors)

    return render_template('profile.html', form=form)