from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import SubmitField, SelectField, FileField
from wtforms.validators import DataRequired 

class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
    
    
class DropDown(FlaskForm):
    choice = SelectField(choices=[])
    submit = SubmitField()

    def __init__(self, fileLabel, submitLabel='Submit', placeholder=None, choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if choices:
            if placeholder:
                self.choice.choices.append(('', placeholder))
            self.choice.choices.extend(choices)
        
        self.choice.label.text = fileLabel
        self.submit.label.text = submitLabel