from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

class FilePicker(FlaskForm):
    file = SelectField('Pick File To Analyze', choices=[('1', '1'), ('2', '2'), ('3', '3')])
    submit = SubmitField('Submit')