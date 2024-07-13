from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from ... import db
from flask_login import login_user, login_required, logout_user, current_user

AuthBP = Blueprint('auth', __name__)
PATH = 'auth/'
@AuthBP.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.user_type == 'admin':
            pass
        else:
            return redirect(url_for('main.homepage'))
    
    path = PATH + 'login.html'
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.homepage'))
            else:
                flash('Incorrect information, try again', category='error')
        else:
            flash('Incorrect information, try again', category='error')
            
    return render_template(path, user=current_user)

@AuthBP.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@AuthBP.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    path = PATH + 'signup.html'
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Account already exists', category='error')  
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            newUser = User(email=email, firstName=firstName, password=generate_password_hash(password1))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('main.homepage'))
        
    return render_template(path, user=current_user)


