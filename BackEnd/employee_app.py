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
from flask_login import (
    login_user,
    current_user,
    LoginManager,
    logout_user,
    login_required,
    login_manager)
from flask_pymongo import PyMongo
from employee_app.auth import auth
from employee_app.dash import dash
from models.employer import Employer
from models.employee import Employee
from models.user import User
from models.forms import LoginForm
from models.forms import RegisterForm
from models.utils import time_date, hash_pwd, check_pwd
from datetime import datetime, timedelta, date
from dateutil.parser import parse
import requests
import pymongo
from bson import ObjectId
import os
import sys
import json


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


"""App configutation"""
template_dir = os.path.abspath('FrontEnd/templates')
static_dir = os.path.abspath('FrontEnd/static')
employee_app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir)
employee_app.config["SECRET_KEY"] = configuration["FLASK_SECRET_KEY"]
employee_app.secret_key = configuration["FLASK_SECRET_KEY"]
employee_app.config["MONGO_URI"] = configuration["MONGO_URI"]
employee_app.config['SESSION_COOKIE_NAME'] = 'employee-login-session'
mongo = PyMongo(employee_app)
"""Login Manager
"""
login_manager = LoginManager()
login_manager.init_app(employee_app)
login_manager.login_view = 'auth.login'
login_manager.login_message = u"Please Login!"
login_manager.login_message_category = "flash-error"


"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employee = db["Employees"]
col_calendar = db["Calendar"]


@login_manager.user_loader
def load_user(user_id):
    """load_user is essential
    for login in user
    """
    user_check = col_employee.find_one({'_id': ObjectId(user_id)})
    return User(user_check)


@employee_app.context_processor
def some_processor():
    def week_s_e(sunday):
        """custom jinja processor"""
        l = sunday.split("-")
        s_day = date(int(l[0]), int(l[1]), int(l[2]))
        s_month = s_day.strftime("%b")
        start_day = s_day.strftime("%d")
        e_day = s_day + timedelta(days=6)
        e_month = e_day.strftime("%b")
        end_day = e_day.strftime("%d")

        s_e_w =  "{} {} - {} {}".format(s_month, start_day, e_month, end_day)
        return s_e_w
    return {'week_s_e': week_s_e}


"""register Blueprints to app"""
employee_app.register_blueprint(auth)
employee_app.register_blueprint(dash)


@employee_app.route('/', strict_slashes=False)
def landin_page():
    """Landing Pages
    """
    return 'Landing Page'


if __name__ == "__main__":
    employee_app.run(
        host=configuration["EM_HOST"],
        port=configuration["EM_PORT"],
        debug=True
    )
