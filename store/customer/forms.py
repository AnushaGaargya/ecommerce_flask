from wtforms import Form,StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError, IntegerField
from flask_wtf.file import file_allowed, file_required, FileField
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name: ')
    username = StringField('Username: ', [validators.DataRequired()])
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ', [validators.DataRequired(), validators.EqualTo('confirm', message='Both passwords must match!')])
    confirm = PasswordField('Repeat Password: ', [validators.DataRequired()])
    # country = StringField('Country: ', [validators.DataRequired()])
    state = StringField('State: ', [validators.DataRequired()])
    city = StringField('City: ', [validators.DataRequired()])
    contact = IntegerField('Contact: ', [validators.DataRequired()])
    address = StringField('Address: ', [validators.DataRequired()]) 
    zipcode = IntegerField('Zipcode: ', [validators.DataRequired()]) 
    # profile = FileField('Profile', validators=[file_allowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only')])
    submit = SubmitField('Register')

    def validate_username(self, username):   
        if Register.query.filter_by(username=username.data).first():
            raise ValidationError('This username is already in use')


    def validate_email(self, email):
        if Register.query.filter_by(email=email.data).first():
            raise ValidationError('This email is already in use')
        

class CustomerLoginForm(FlaskForm):
    email = StringField('Email: ', [validators.Email(), validators.DataRequired()])
    password = PasswordField('Password: ',[validators.DataRequired()])
  

