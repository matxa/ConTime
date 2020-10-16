#!/usr/bin/env python3
"""Auth routes
"""
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    url_for,
    Blueprint,
    make_response,
    render_template,
    flash)
from flask_pymongo import PyMongo
from flask_login import (
    login_user,
    current_user,
    LoginManager,
    logout_user,
    login_required,
    login_manager)
from models.utils import (
    today_date,
    hash_pwd,
    check_pwd)
from models.forms import (
    LoginForm,
    RegisterForm)
from models.employer import Employer
from models.user import User
import requests
import pymongo
from bson import ObjectId
import os
import sys
import json


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


auth = Blueprint('auth', __name__, url_prefix='/auth')
"""Login Manager and MngoDB
"""
login_manager = LoginManager()
login_manager.init_app(auth)
login_manager.login_view = 'login'
# DB
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]


@auth.route('/register', strict_slashes=False, methods=['GET', 'POST'])
def register():
    """Register User
    if non existent
    """
    form = RegisterForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            new_employer = Employer(
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                hash_pwd(form.password.data))
            req = requests.post(
                'http://{}/api/employer'.format(configuration["TEST_HOST"]),
                json=new_employer.object()
            )
            if req.status_code == 303 or req.status_code == 400:
                flash("User already exists")
                return redirect(url_for('auth.register'))
            else:
                flash("Account successfully created. Login!", 'flash-success')
                return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form)


@login_manager.user_loader
def load_user(user_id):
    """load_user is essential
    for login in user
    """
    user_check = col_employer.find_one({'_id': ObjectId(user_id)})
    return User(user_check)


@auth.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    """Login route checks if user is
    authenticated and ready to login
    """

    form = LoginForm()

    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('dash.dashboard'))
        return render_template('login.html', title='Login', form=form)

    if form.validate_on_submit():
        # look for email in database
        user_check = col_employer.find_one({"email": form.email.data})
        # check if user exists if so check pwd to database hash pwd
        if user_check is not None and check_pwd(
         form.password.data, user_check["password"]):
            employer_user = User(user_check)
            # log user in
            login_user(employer_user)
            redirect(url_for('dash.dashboard'))

    return redirect(url_for('auth.login'))


@auth.route('/logout', strict_slashes=False, methods=['GET', 'POST'])
def logout():
    """log user out
    with a message
    """
    if current_user.is_active:
        logout_user()
        flash("You've logged out", 'flash-success')
    else:
        flash("You aren't logged in", 'flash-error')
    return redirect(url_for('auth.login'))
