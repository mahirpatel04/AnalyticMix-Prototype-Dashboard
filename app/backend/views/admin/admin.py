from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import User, CSV
from werkzeug.security import generate_password_hash, check_password_hash 
from ... import db
from flask_login import login_user, login_required, logout_user, current_user
from ..forms.forms import DropDown, CheckBox
from ...scripts.processing import getColumns, process, convertBinaryFileToDataFrame
from sklearn.linear_model import LinearRegression



AdminBP = Blueprint('AdminBP', __name__, url_prefix='/admin')

# Admin Homepage
@AdminBP.route('/home')
@login_required
def homepage():
    path = 'admin/admin_base.html'
    return render_template(path, user=current_user)

# Choose User
@AdminBP.route('/choose_user', methods=['GET', 'POST'])
@login_required
def choose_user():
    path = 'admin/choose_user.html'
    if request.method == 'POST':
        selected_user_id = request.form.get('choice')
        if selected_user_id == '' or selected_user_id == None:
            flash('Please select a valid user!', 'error')
            return redirect(url_for('AdminBP.choose_user'))
        else:
            return redirect(url_for('AdminBP.choose_file', user=selected_user_id))
        
    general_users = User.query.filter_by(user_type='user').all()
    choices = [(user.id, user.firstName) for user in general_users]
    
    form = DropDown(choiceLabel='Choose User', choices=choices, placeholder='Pick One User:')
    
    return render_template(path, form=form, potentialUsers=general_users, user=current_user)

@AdminBP.route('/choose_file', methods=['GET', 'POST'])
@login_required
def choose_file():
    path = 'admin/choose_file.html'

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
    form = DropDown(choiceLabel='Choose File', choices=choices, placeholder=f'Files uploaded by {userObject.firstName}:')
    
    return render_template(path, user=current_user, form=form, userID=userID)


@AdminBP.route('/analyze_file', methods=['GET', 'POST'])
@login_required
def analyze_file():
    path = 'admin/analyze_file.html'    
    userID = request.args.get('userID')
    fileID = request.args.get('file')
    fileObject = CSV.query.filter_by(userID=userID, id=fileID).first()
    df = convertBinaryFileToDataFrame(fileObject.data)
    if request.method == 'POST':
        independentVars = request.form.getlist('choice1')
        dependentVars = request.form.getlist('choice2')
        models = request.form.getlist('choice3')
        result = process(df, independentVars, dependentVars, models)
        return result
        
    choices = getColumns(df)
    models = [(LinearRegression, 'Linear')]
    form = CheckBox(label1='Choose Independent Variables', label2='Choose Dependent Variables', label3='Choose Models to Run',
                    choices1=choices, choices2=choices, choices3=models)

    return render_template(path, user=current_user, form=form, userID=userID, fileID=fileID)

@AdminBP.route('/view_data', methods=['GET', 'POST'])
@login_required
def view_data():
    userID = request.args.get('userID')
    fileID = request.args.get('fileID')
    
    # Fetch the file data from the database
    fileObject = CSV.query.filter_by(userID=userID, id=fileID).first()
    df = convertBinaryFileToDataFrame(fileObject.data)
    
    # Convert the DataFrame to HTML
    df_html = df.to_html(classes='table table-striped table-bordered', index=False)
    
    path = 'admin/view_data.html'
    return render_template(path, user=current_user, data_html=df_html, userID=userID, fileID=fileID)


@AdminBP.route('/view_corr', methods=['GET', 'POST'])
@login_required
def view_corr():
    userID = request.args.get('userID')
    fileID = request.args.get('fileID')
    
    # Fetch the file data from the database
    fileObject = CSV.query.filter_by(userID=userID, id=fileID).first()
    df = convertBinaryFileToDataFrame(fileObject.data)
    
    # Convert the DataFrame to HTML
    newDf = df.drop(columns='ordine_data')
    correlationTable = newDf.corr()
    corr_html = correlationTable.to_html(classes='table table-striped table-bordered')
    path = 'admin/view_corr.html'
    return render_template(path, user=current_user, data_html=corr_html, userID=userID, fileID=fileID)