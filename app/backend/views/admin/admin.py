from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import User, CSV
from werkzeug.security import generate_password_hash, check_password_hash 
from ... import db
from flask_login import login_user, login_required, logout_user, current_user
from ..forms.forms import DropDown
from ...scripts.processing import process


AdminBP = Blueprint('AdminBP', __name__, url_prefix='/admin')
PATH = 'admin/'


@AdminBP.route('/home')
@login_required
def homepage():
    path = PATH + 'admin_home.html'
    return render_template(path, user=current_user)


@AdminBP.route('/choose_user', methods=['GET', 'POST'])
@login_required
def choose_user():
    path = PATH + 'choose_user.html'
    if request.method == 'POST':
        selected_user_id = request.form.get('choice')
        if selected_user_id == '' or selected_user_id == None:
            flash('Please select a valid user!', 'error')
            return redirect(url_for('AdminBP.choose_user'))
        else:
            return redirect(url_for('AdminBP.choose_file', user=selected_user_id))
        
    general_users = User.query.filter_by(user_type='user').all()
    choices = [(user.id, user.firstName) for user in general_users]
    
    form = DropDown(fileLabel='Choose User', choices=choices, placeholder='Pick One User:')
    
    return render_template(path, form=form, potentialUsers=general_users, user=current_user)

@AdminBP.route('/choose_file', methods=['GET', 'POST'])
@login_required
def choose_file():
    path = PATH + 'choose_file.html'

    userID = request.args.get('user')
    userObject = User.query.filter_by(id=userID).first()
    if request.method == 'POST':
        selected_file_id = request.form.get('choice')
        if selected_file_id == '' or selected_file_id == None:
            flash('Please select a valid file!', 'error')
            return redirect(url_for('AdminBP.choose_file', user=userID))
        else:
            return redirect(url_for('AdminBP.analyze_file', userID=userID, file=selected_file_id))
        
    choices = [(file.id, file.fileName) for file in userObject.files]
    form = DropDown(fileLabel='Choose File', choices=choices, placeholder=f'Files uploaded by {userObject.firstName}:')
    
    return render_template(path, user=current_user, form=form)


@AdminBP.route('/analyze_file', methods=['GET'])
@login_required
def analyze_file():
    path = PATH + 'analyze_file.html'
    userID = request.args.get('userID')
    fileID = request.args.get('file')
    fileObject = CSV.query.filter_by(userID=userID, id=fileID).first()
    fileData = process(fileObject.data)
    return render_template(path, user=current_user, file=fileData)