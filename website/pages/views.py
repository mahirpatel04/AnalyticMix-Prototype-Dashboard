from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from ..scripts.csvprocessing import process_csv
from os import path
from ..database.models import CSV
from .. import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)



ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        upload = CSV(fileName=file.filename, data=file.read(), userID = current_user.id)
        db.session.add(upload)
        db.session.commit()
        return render_template('upload.html', user=current_user)

    return render_template('upload.html', user=current_user)


@views.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', user=current_user)