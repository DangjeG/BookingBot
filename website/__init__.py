from flask import Flask, session, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from os import path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bread'

db = SQLAlchemy()
DB_NAME = "database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
db.init_app(app)

app.jinja_env.globals.update(BOTID = 5903687838) #айди бота из токена до знака ":"
app.jinja_env.globals.update(BOTNAME = "BookingBot") #имя вашего бота с приставкой bot
app.jinja_env.globals.update(BOTDOMAIN = "http://127.0.0.1:5000") #домен вашего сайта из /setdomain в BotFather (обычно http://127.0.0.1:5000)

from website import routes

from .models import User
with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')