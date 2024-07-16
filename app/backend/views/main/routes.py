from flask import Blueprint, render_template, redirect, url_for
from flask_login import  current_user

MainBP = Blueprint('MainBP', __name__)

@MainBP.route('/')
def homepage():
    if current_user.is_authenticated:
        if current_user.user_type == 'admin':
            return redirect(url_for('AdminBP.homepage'))
    return render_template('main.html', user=current_user)