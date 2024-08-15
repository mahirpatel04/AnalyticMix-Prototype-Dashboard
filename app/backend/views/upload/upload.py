from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ...models import CSV
from backend import db
from ..forms.forms import UploadForm

UploadBP = Blueprint('upload', __name__)
PATH = 'upload/'
ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@UploadBP.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    path = PATH + 'upload.html'
    form = UploadForm()
    if request.method == 'POST':
        file = form.file.data
        print("Received file:", file.filename)
        
        if not allowed_file(file.filename):
            raise TypeError("File type not allowed")
        
        upload = CSV(fileName=file.filename, data=file.read(), userID=current_user.id)
        db.session.add(upload)
        db.session.commit()
        print("File saved successfully:", file.filename)
        return render_template(path, user=current_user, form=form)
    
    return render_template(path, user=current_user, form=form)