from flask import Blueprint, render_template
from flask_login import login_required, current_user

analytics = Blueprint('analytics', __name__)
PATH = 'analytics/'
@analytics.route('/analytics')
@login_required
def analytics_page():
    path = PATH + 'analytics.html'
    return render_template(path, user=current_user)