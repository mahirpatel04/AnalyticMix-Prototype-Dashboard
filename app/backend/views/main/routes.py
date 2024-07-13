from flask import Blueprint, render_template
from flask_login import  current_user

MainBP = Blueprint('main', __name__)

@MainBP.route('/')
def homepage():
    return render_template('main.html', user=current_user)