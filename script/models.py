from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import request
import json
import string
import random

from main import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    joined_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    # Function to hash password before pushing into database
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Function to compare password from input password with hashed password from database
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

