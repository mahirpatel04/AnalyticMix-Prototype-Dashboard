from flask_login import current_user
from flask import render_template, Blueprint

ErrorBP = Blueprint('ErrorBP', __name__)
PATH = 'error/'
@ErrorBP.app_errorhandler(404)
def not_found(e):
    path = PATH + 'error.html'
    return render_template(path, user=current_user), 404