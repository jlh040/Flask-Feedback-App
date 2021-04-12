from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email

class RegisterForm(FlaskForm):
    """Form to register a user."""

    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])

class LoginForm(FlaskForm):
    """Form to log a user in."""
    username = StringField('Username:', validators=[InputRequired()])
    
    password = PasswordField('Password:', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Form to add feedback for a user."""
    title = StringField('Enter The Title', validators=[InputRequired()])
    content = TextAreaField('Enter Your Feedback:', validators=[InputRequired()])