from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from models.models import User

class FeedbackForm(FlaskForm):
    
    firstname = StringField(label='First Username', validators=[Length(min=2, max=20), DataRequired()])
    lastname = StringField(label='Last Username', validators=[Length(min=2, max=20), DataRequired()])
    feedback = StringField(label='Enter your feedback', validators=[Length(min=10, max=200), DataRequired()])
    department = StringField(label='Department Name', validators=[Length(max=200), DataRequired()])
    position = StringField(label='Postion of Employee', validators=[Length(max=200), DataRequired()])
    submit = SubmitField(label='Submit')

class RegisterForm(FlaskForm):
    firstname = StringField(label='First Name', validators=[Length(min=2, max=20), DataRequired()])
    lastname = StringField(label='Last Name', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6, max=60), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_firstname(self, firstname_to_check):
        user_by_firstname = User.query.filter_by(firstname=firstname_to_check.data).first()
        if user_by_firstname:
            raise ValidationError('Account already exists with this first name')

    def validate_lastname(self, lastname_to_check):
        user_by_lastname = User.query.filter_by(lastname=lastname_to_check.data).first()
        if user_by_lastname:
            raise ValidationError('Account already exists with this last name')

    def validate_email(self, email_to_check):
        user_by_email = User.query.filter_by(email=email_to_check.data).first()
        if user_by_email:
            raise ValidationError('Account already exists with this email address')

class LoginForm(FlaskForm):
    firstname = StringField(label='First Username', validators=[DataRequired()])
    lastname = StringField(label='Last Username', validators=[DataRequired()])
    password = PasswordField(label = 'Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

    