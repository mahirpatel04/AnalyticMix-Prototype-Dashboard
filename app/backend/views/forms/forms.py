from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import SubmitField, SelectField, FileField, SelectMultipleField, widgets
from wtforms.validators import DataRequired 

class UploadForm(FlaskForm):
    file = FileField('File', validators=[DataRequired()])
    submit = SubmitField('Upload')
    
    
class DropDown(FlaskForm):
    choice = SelectField(choices=[])
    submit = SubmitField()

    def __init__(self, choiceLabel, submitLabel='Submit', placeholder=None, choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if choices:
            if placeholder:
                self.choice.choices.append(('', placeholder))
            self.choice.choices.extend(choices)
        
        self.choice.label.text = choiceLabel
        self.submit.label.text = submitLabel

class CheckBox(FlaskForm):
    choice1 = SelectMultipleField(choices=[], 
                                 widget = widgets.ListWidget(prefix_label=False),
                                 option_widget = widgets.CheckboxInput())
    choice2 = SelectMultipleField(choices=[], 
                                 widget = widgets.ListWidget(prefix_label=False),
                                 option_widget = widgets.CheckboxInput())
    choice3 = SelectMultipleField(choices=[], 
                                 widget = widgets.ListWidget(prefix_label=False),
                                 option_widget = widgets.CheckboxInput())
    submit = SubmitField()
    def __init__(self, label1, label2, label3, submitLabel='Submit', placeholder=None, choices1=None, choices2=None, choices3=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if choices1 and choices2 and choices3:
            if placeholder:
                self.choice1.choices.append(('', placeholder))
            self.choice1.choices.extend(choices1)
            self.choice2.choices.extend(choices2)
            self.choice3.choices.extend(choices3)
        
        self.choice1.label.text = label1
        self.choice2.label.text = label2
        self.choice3.label.text = label3
        
        self.submit.label.text = submitLabel