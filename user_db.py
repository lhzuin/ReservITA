from flask_wtf import FlaskForm
import validators
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask import render_template
from app import app


from app import LoginForm



def valid_login(username, password):

    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])

    form = LoginForm()

    if form.validate_on_submit():
        print(form.username.data)
        print(form.password.data)
        return True
    else:
        print(form.errors)
        return False    

    return render_template('form.html', form=form)
class User:
    def __init(self, name, phone, email, password, priority, status):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.priority = priority
        self.status = status