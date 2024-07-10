from flask import Blueprint, render_template
from flask_login import login_required, current_user


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html', user=current_user)


@views.route('/upload')
@login_required
def upload():
    return render_template('upload.html', user=current_user)


@views.route('/analytics')
@login_required
def analytics():
    return render_template('analytics.html', user=current_user)