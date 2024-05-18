"""
    Handle profile accessing and rerouting on login condition
"""

from sqlalchemy.exc import IntegrityError
from database.models import db, User, Session
from jinja2 import TemplateNotFound

from flask import (
    current_app, Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify, abort
)

import database.routes

user = Blueprint('user', __name__, url_prefix='/user', template_folder='templates')

@user.route('/')
def showUser():

    try:
        return render_template('user.html')
    except TemplateNotFound:
        abort(404)