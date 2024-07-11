from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from os import path
from ...models import CSV
from ... import db


upload = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        upload = CSV(fileName=file.filename, data=file.read(), userID = current_user.id)
        db.session.add(upload)
        db.session.commit()
        return render_template('upload.html', user=current_user)

    return render_template('upload.html', user=current_user)