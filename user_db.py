from flask import render_template
from werkzeug.security import generate_password_hash, check_password_hash


def valid_login(username, password):
    return True
    #return db.session.query(User).filter(User.username == username and User.password == password).count() != 0

class User:
    def __init(self, name, password):
        self.username = name
        self.password = password