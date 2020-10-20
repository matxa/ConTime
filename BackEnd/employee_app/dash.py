"""Flask imports"""
from flask import (
    Flask,
    request,
    jsonify,
    redirect,
    url_for,
    make_response,
    Blueprint,
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
from models.utils import today_date, strip_date, hash_pwd, check_pwd
from models.forms import AddEmployee, ChangepwdForm
import requests
import pymongo
import os
import sys
import json


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]
col_employee = db["Employee"]


employee = Blueprint('employee', __name__)


@employee.route('/employeecalendar', strict_slashes=False, methods=['GET', "POST"])
def employees_page():
    """Employees portal page
    """
    return render_template(
        'employeecalendar.html',
        title="Calendar",
        current_date=today_date()
    )
