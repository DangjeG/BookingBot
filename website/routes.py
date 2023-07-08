from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_required, logout_user
from . import app

@app.before_request
def make_session_permanent():
    session.permanent = True

def template(tmpl_name, **kwargs):
    telegram = False
    user_id = session.get('user_id')
    username = session.get('name')
    photo = session.get('photo')

    if user_id:
        telegram = True

    return render_template(tmpl_name,
                           telegram = telegram,
                           user_id = user_id,
                           name = username,
                           photo = photo,
                           **kwargs)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/tglogin')
def tglogin():
    user_id = request.args.get("id")
    first_name = request.args.get("first_name")
    photo_url = request.args.get("photo_url")

    session['user_id'] = user_id
    session['name'] = first_name
    session['photo'] = photo_url

    return redirect(url_for('views'))

@app.route('/logout')
@login_required
def logout():
    session.pop("user_id")
    session.pop("name")
    session.pop("photo")

    return redirect(url_for('views'))