from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(nickname) < 5:
            flash('Имя пользователя должно быть больше 5 символов', category='error')
        elif len(nickname) > 32:
            flash('Имя пользователя должно быть меньше 32 символов', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают', category='error')
        else:
            flash('Account created!', category='success')
    return render_template("signup.html", user=current_user)
