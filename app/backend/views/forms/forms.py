from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import *
from wtforms.validators import *

class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
    
    
class DropDown(FlaskForm):
        file = SelectField(label='Pick File To Analyze', choices=[('1', '1'), ('2', '2'), ('3', '3')])
        submit = SubmitField('Submit')