from os import path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bread'

db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

app.jinja_env.globals.update(BOTID=5903687838)
app.jinja_env.globals.update(BOTNAME="BookingBot")
app.jinja_env.globals.update(BOTDOMAIN="http://127.0.0.1:5000")

from website import routes

from .models import User

with app.app_context():
    db.create_all()


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
