from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField, IntegerField, SelectField, 
    SelectMultipleField, widgets, SubmitField, PasswordField
)
from wtforms.validators import DataRequired, NumberRange, Length, EqualTo

class MultiCheckboxField(SelectMultipleField):
    """Custom field for multiple checkbox selection with custom widget."""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class TestTemplateForm(FlaskForm):
    """Form for creating a math test template."""
    title = StringField('Test Title', validators=[DataRequired(), Length(min=3, max=100)])
    description = TextAreaField('Description (Optional)', validators=[Length(max=500)])
    
    difficulty = SelectField(
        'Difficulty Level', 
        choices=[
            ('easy', 'Easy'), 
            ('medium', 'Medium'), 
            ('hard', 'Hard')
        ],
        validators=[DataRequired()]
    )
    
    topics = MultiCheckboxField(
        'Math Topics', 
        choices=[
            ('addition', 'Addition'),
            ('subtraction', 'Subtraction'),
            ('multiplication', 'Multiplication'),
            ('division', 'Division'),
            ('fractions', 'Fractions'),
            ('decimals', 'Decimals'),
            ('percentages', 'Percentages'),
            ('algebra', 'Basic Algebra'),
            ('geometry', 'Basic Geometry'),
            ('statistics', 'Basic Statistics')
        ],
        validators=[Length(min=1, message="Please select at least one topic")]
    )
    
    num_questions = IntegerField(
        'Number of Questions', 
        validators=[
            DataRequired(), 
            NumberRange(min=1, max=50, message='Please enter a number between 1 and 50')
        ]
    )
    
    num_versions = IntegerField(
        'Number of Unique Test Versions', 
        validators=[
            DataRequired(), 
            NumberRange(min=1, max=100, message='Please enter a number between 1 and 100')
        ],
        default=1
    )
    
    password = PasswordField(
        'Answer Key Access Password', 
        validators=[
            DataRequired(), 
            Length(min=6, message='Password must be at least 6 characters long')
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match')
        ]
    )
    
    submit = SubmitField('Generate Tests')

class AnswerKeyAccessForm(FlaskForm):
    """Form for accessing a test's answer key."""
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Access Answer Key')
