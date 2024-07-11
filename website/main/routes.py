from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from os import path
from ..models import CSV
from .. import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('main.html', user=current_user)