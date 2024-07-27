from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ...scripts.processing import fig
from ..forms.forms import DropDown


AnalyticsBP = Blueprint('analytics', __name__)
PATH = 'analytics/'


@AnalyticsBP.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics_page():
    path = PATH + 'analytics.html'
    path = PATH + 'analytics.html'
    form = DropDown(fileLabel='Pick a file to analyze', choiceLabel='Choice', choices=['1', '1'])
    file = None

    if request.method == 'POST':
        file = form.choice.data
        return render_template(path, fig=fig, user=current_user, file=file, form=form)
    
    return render_template(path, fig=fig, user=current_user, file=file, form=form)