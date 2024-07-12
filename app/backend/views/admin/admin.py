from flask import Blueprint, render_template, request, flash, redirect, url_for
from ...models import User
from werkzeug.security import generate_password_hash, check_password_hash 
from ... import db
from flask_login import login_user, login_required, logout_user, current_user


AdminBP = Blueprint('AdminBP', __name__)
PATH = 'admin/'


@AdminBP.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    path = PATH + 'admin.html'
    return render_template(path, user=current_user)