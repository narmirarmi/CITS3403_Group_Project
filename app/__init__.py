from flask import Blueprint

login_bp = Blueprint('login', __name__)
logout_bp = Blueprint('logout', __name__)
register_bp = Blueprint('register', __name__)
settings_bp = Blueprint('settings', __name__)
profile_bp = Blueprint('profile', __name__)
upload_photo_bp = Blueprint('upload_photo', __name__)

from . import routes