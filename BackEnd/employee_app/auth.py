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
    time_date,
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
import bson


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


auth = Blueprint('auth', __name__)


"""Login Manager and MngoDB
"""
login_manager = LoginManager()
login_manager.init_app(auth)
login_manager.login_view = 'auth.login'
login_manager.login_message = u"Please Login!"
login_manager.login_message_category = "flash-error"
# DB
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employee = db["Employees"]


@login_manager.user_loader
def load_user(user_id):
    """load_user is essential
    for login in user
    """
    user_check = col_employee.find_one({'_id': ObjectId(user_id)})
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
        return render_template('employee_login.html', title='Login', form=form)

    if form.validate_on_submit():
        # look for email in database

        if bson.objectid.ObjectId.is_valid(form.password.data):
            user_check = col_employee.find_one({"_id": ObjectId(form.password.data)})
        else:
            flash("Invalid password", 'flash-error')
            return redirect(url_for('auth.login'))
        # check if user exists if so check pwd to database hash pwd
        if user_check is None:
            flash("Account doesn't exist", 'flash-error')
            return redirect(url_for('auth.login'))

        if user_check is not None and form.email.data == user_check["email"]:
            employee_user = User(user_check)
            # log user in
            login_user(employee_user)
            redirect(url_for('dash.dashboard'))
        else:
            flash('Invalid password', 'flash-error')

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
