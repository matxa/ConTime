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
from APP.auth_routes import auth
from APP.dashboard import dash
from models.employer import Employer
from models.employee import Employee
from models.user import User
from models.forms import LoginForm
from models.forms import RegisterForm
from models.utils import time_date
from models.utils import hash_pwd, check_pwd
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
template_dir = os.path.abspath('/root/ConTime/FrontEnd/templates')
static_dir = os.path.abspath('/root/ConTime/FrontEnd/static')
app = Flask(
    __name__,
    template_folder=template_dir,
    static_folder=static_dir)
app.config["SECRET_KEY"] = configuration["FLASK_SECRET_KEY"]
app.secret_key = configuration["FLASK_SECRET_KEY"]
app.config["MONGO_URI"] = configuration["MONGO_URI"]
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
mongo = PyMongo(app)
"""Login Manager
"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = u"Please Login!"
login_manager.login_message_category = "flash-error"


@login_manager.user_loader
def load_user(user_id):
    """load_user is essential
    for login in user
    """
    user_check = col_employer.find_one({'_id': ObjectId(user_id)})
    return User(user_check)


"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]


"""register Blueprints to app"""
app.register_blueprint(auth)
app.register_blueprint(dash)


@app.context_processor
def some_processor():
    def get_name(em_id):
        """custom jinja processor"""
        req = requests.get(
            "http://{}/employee/{}".format(
                configuration["API_TEST_HOST"], em_id)
            )

        return req.json()["first_name"], req.json()["last_name"]

    def week_s_e(sunday):
        """custom jinja processor"""
        ls_sunday = sunday.split("-")
        s_day = date(int(ls_sunday[0]), int(ls_sunday[1]), int(ls_sunday[2]))
        s_month = s_day.strftime("%b")
        start_day = s_day.strftime("%d")
        e_day = s_day + timedelta(days=6)
        e_month = e_day.strftime("%b")
        end_day = e_day.strftime("%d")

        s_e_w = "{} {} - {} {}".format(s_month, start_day, e_month, end_day)
        return s_e_w
    return {
        'get_name': get_name,
        'week_s_e': week_s_e,
        }


@app.route('/', strict_slashes=False)
def landin_page():
    """Landing Pages
    """
    return 'Landing Page'


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        #host=configuration["APP_HOST"],
        #port=configuration["APP_PORT"],
        debug=True
    )
