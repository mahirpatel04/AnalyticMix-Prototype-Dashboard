from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from os import path
from ...models import CSV
from ... import db

analytics = Blueprint('analytics', __name__)
PATH = 'analytics/'
@analytics.route('/analytics')
@login_required
def analytics_page():
    path = PATH + 'analytics_page.html'
    return render_template(path, user=current_user)