from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'jpg', 'png', 'jpeg'}

# create destination form
class DestinationForm(FlaskForm):
    name = StringField('country', validators=[InputRequired()])

    description = TextAreaField('description', validators=[InputRequired()])
    
    image = FileField('cover image', validators=[
        FileRequired(message='Please upload a file'),
        FileAllowed(ALLOWED_FILE, message='Only support png, jpg, jpeg')
        ])
    submit = SubmitField('Create')

# login form
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])
    submit = SubmitField('Login')

# register form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email',  validators=[Email("Please enter a valid email")])

    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")

    submit = SubmitField("Register")

# post comment form
class CommentForm(FlaskForm):
    text = TextAreaField('text', validators=[InputRequired()])
    submit = SubmitField('Post')