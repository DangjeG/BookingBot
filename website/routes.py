from flask import redirect, render_template, request, session
from flask_login import LoginManager, login_required
from Backend.ObjectModels.user_request import UserRequest

from . import app
from .models import User

from Backend.parserexecutor import ParserExecutor


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
    print(float(request.form.get('lat')), float(request.form.get('lng')))
    user_request = UserRequest(
        user_id = request.args.get("id"),
        user_point = (float(request.form.get('lat')), float(request.form.get('lng'))),
        radius_km = request.form.get('radius_km'),
        date_in = request.form.get('date_in'),
        date_out = request.form.get('date_out'),
        adults = request.form.get('adults'),
        children_ages = children_ages(),
        stars = stars(),
        meal_types = mealtype(),
        price = f"{request.form.get('min_price')}-{request.form.get('max_price')}",
        services = services()
    )
    hotels = ParserExecutor.get_hotels(user_request)
    return render_template('hotels.html', hotels=hotels)

def children_ages():
    ages = []
    first = request.form.get('first')
    if first:
        ages.append(first)
    second = request.form.get('second')
    if second:
        ages.append(second)
    third = request.form.get('third')
    if third:
        ages.append(third)
    return ages

def stars():
    stars = []
    for i in range(6):
        star = request.form.get(str(i))
        if star:
            stars.append(star)

    return stars

def mealtype():
    meal_types = []
    for i in range(1, 6):
        type = request.form.get(f'type{i}')
        if type:
            meal_types.append(type)
    return meal_types

def services():
    services = []
    for i in range(1, 8):
        service = request.form.get(f'service{i}')
        if service:
            services.append(service)
    return services