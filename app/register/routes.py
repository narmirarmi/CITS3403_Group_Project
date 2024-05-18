from flask import Blueprint, flash, render_template, redirect, url_for
from app.webforms import RegisterForm, User, db
from flask_bcrypt import Bcrypt

# Create a Blueprint
register_bp = Blueprint('register', __name__, url_prefix='/register')

bcrypt = Bcrypt()

@register_bp.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            password=hashed_password,
            email=form.email.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('You have been registered successfully.', 'success')
        return redirect(url_for('login.login'))

    return render_template('register.html', form=form)