from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import FileField, StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    about = db.Column(db.String(500), nullable=True)
    profile_pic = db.Column(db.String(), nullable=True)

    images = db.relationship('Image', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy=True)
    followees = db.relationship('Follow', foreign_keys='Follow.followee_id', backref='followee', lazy=True)

    def get_id(self):
        return str(self.user_id)
    
    def get_profile_picture(self):
        if self.profile_picture:
            return self.profile_picture
        else:
            return "UPLOAD_FOLDER/user-icon.png"

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    votes = db.relationship('Vote', backref='image', lazy=True)
    comments = db.relationship('Comment', backref='image', lazy=True)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    type = db.Column(db.Enum('like', 'dislike'), nullable=False)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    comment_date = db.Column(db.DateTime, default=datetime.utcnow)

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    followee_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

class RegisterForm(FlaskForm):
    first_name = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "FirstName"})
    last_name = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "LastName"})
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=100)], render_kw={"placeholder": "Password"})
    email = StringField(validators=[InputRequired(), Email(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()

        if existing_user_username:
            raise ValidationError("This username already exists! Please choose a different one.")
        
    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError("This email already exists! Please choose a different one.")

class UpdateForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "First Name"})
    last_name = StringField('Last Name', validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Last Name"})
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=50)], render_kw={"placeholder": "Email"})
    about = StringField('About', validators=[Length(min=0, max=500)], render_kw={"placeholder": "About Me"})
    profile_pic = FileField('Profile Picture')
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password')
    
    submit = SubmitField("Save Changes")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=50)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8, max=100)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class ImageForm(FlaskForm):
    image_path = FileField('Upload Image', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Upload')