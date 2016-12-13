__author__ = 'mmtbz'
from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import TextField

class RegistrationForm(Form):  # this means this class inherits Form
    email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password', validators=[validators.DataRequired(), validators.Length(min=8,
                                                                                                  message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2', validators=[validators.DataRequired(),
                                                       validators.EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Sign Up!', [validators.DataRequired()])


class LoginForm(Form):
    LoginEmail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    LoginPwd = PasswordField('password', validators=[validators.DataRequired(message="Password field is required")])
    submit = SubmitField('Log In', [validators.DataRequired(message="Please fill in all the fields")])


class CreateTableForm(Form):
    tableNumber = TextField('Table Number', validators=[validators.DataRequired()])
    submit = SubmitField('createtablesubmit', [validators.DataRequired])
