from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from ... import db
from flask_login import login_user, login_required, logout_user, current_user


AdminBP = Blueprint('AdminBP', __name__, url_prefix='/admin')
PATH = 'admin/'


@AdminBP.route('/home')
@login_required
def admin():
    path = PATH + 'admin_home.html'
    return render_template(path, user=current_user)


