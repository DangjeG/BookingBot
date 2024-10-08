from flask_login import UserMixin

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=32), nullable=False, unique=True)
    password = db.Column(db.String(length=32), nullable=False)
