from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash


def valid_login(username, password):
    #return True
    user = User.query.filter_by( user.username).first()

    if not user or not check_password_hash(user.password, password):
        return True
    else:
        return False
class User:
    def __init(self, name, phone, email, password, priority, status):
        self.name = name
        self.phone = phone
        self.email = email
        self.password = password
        self.priority = priority
        self.status = status