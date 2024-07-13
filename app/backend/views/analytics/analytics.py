from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from ...scripts.processing import fig
from ..forms.forms import FilePicker


AnalyticsBP = Blueprint('analytics', __name__)
PATH = 'analytics/'


@AnalyticsBP.route('/analytics', methods=['GET', 'POST'])
@login_required
def analytics_page():
    path = PATH + 'analytics.html'
    file = None
    form = FilePicker()
    return render_template(path, fig=fig, user=current_user, file=file, form=form)