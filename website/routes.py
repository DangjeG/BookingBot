from flask import redirect, render_template, request, session
from flask_login import LoginManager, login_required

from . import app
from .models import User

login_manager = LoginManager()
login_manager.login_view = 'tglogin'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.find_by_session_id(id)


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
# @login_requireds
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

    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    session.pop("user_id")
    session.pop("name")
    session.pop("photo")
    return redirect('/login')


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/hotels', methods=['POST'])
def hotels():
    inputs = request.form.values()
    print( ', '.join(inputs))
    return render_template('hotels.html')