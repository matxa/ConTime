#!/usr/bin/env python3
"""ConTime APP
"""
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    url_for,
    make_response,
    session,
    render_template,
    flash)

from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from api.employer_routes import api
from api.employee_routes import api
from api.calendar_routes import api
from models.employer import Employer
from models.employee import Employee
from datetime import timedelta
from models.forms import LoginForm
from models.forms import RegisterForm
import requests
import pymongo
import os
import sys
import json

"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


"""App configutation"""
template_dir = os.path.abspath('FrontEnd/templates')
static_dir = os.path.abspath('FrontEnd/static')
app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir
    )
app.config["SECRET_KEY"] = configuration["FLASK_SECRET_KEY"]
app.secret_key = configuration["FLASK_SECRET_KEY"]
app.config["MONGO_URI"] = configuration["MONGO_URI"]
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]


"""register Blueprints to app"""
app.register_blueprint(api)

# Home
@app.route('/', strict_slashes=False)
def landin_page():
    return 'Landing Page'

# Register
@app.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_employer = Employer(
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                bcrypt.generate_password_hash(
                    form.password.data).decode('utf-8'))
            req = requests.post(
                'http://192.168.1.9:5050/api/employer',
                json=new_employer.object()
            )
            if req.status_code == 303 or req.status_code == 400:
                flash("User already exists")
                return redirect('register')
            else:
                created_user = req.json()
                session["user"] = created_user
                return redirect(url_for('login'), code=307)

    return render_template('register.html', title='Register', form=form)

# Login
@app.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            usr = session["user"]
            form.email = usr["email"]
            form.password = usr["password"]
            try:
                user = col_employer.find_one({"email": form.email})
                if user is not None and bcrypt.check_password_hash(user["password"], usr["password"]):
                    user = dict(user)
                    del user["_id"]
                    return jsonify(user)
                return jsonify("WRONG")
            except Exception as e:
                return jsonify({"error": str(e)})
            # req = requests.get(
            #     'http://192.168.1.9:5050/api/employer/{}'.format()
            # )
            # return jsonify(req.status_code)

    return render_template('login.html', title='Login', form=form)


@app.route('/dashboard', strict_slashes=False, methods=['GET', 'POST'])
def dashboard():
    """dashBoard
    """
    return render_template('appLayout.html')

if __name__ == "__main__":
    app.run(
        host='192.168.1.9',
        port='5050',
        debug=True
    )
