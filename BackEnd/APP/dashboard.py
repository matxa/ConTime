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
from models.utils import time_date, hash_pwd, check_pwd
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
col_calendar = db["Calendar"]


dash = Blueprint('dash', __name__)


def app_layout():
    """info needed for app
    layout to stay consistent
    """
    """user"""
    req = requests.get(
        "http://{}/employer/{}".format(
            configuration["API_TEST_HOST"], current_user.get_id())
    )
    req_data = req.json()

    """employee count"""
    employee_count = requests.get(
        "http://{}/employer/{}/employee".format(
            configuration["API_TEST_HOST"],
            current_user.get_id())
    )
    count = next(iter(employee_count.json()))

    return (req_data, count)


@dash.route('/dashboard', strict_slashes=False, methods=['GET', "POST"])
@login_required
def dashboard():
    """dashBoard
    """

    past_cal = col_calendar.find({"employer_id": current_user.get_id()})

    return render_template(
        'dashboard.html',
        title="DashBoard",
        current_date=time_date()[0],
        user=app_layout()[0],
        count=app_layout()[1],
        list_of_employee_calendars=past_cal)


@dash.route('/employees', strict_slashes=False, methods=['GET', "POST"])
@login_required
def employers_employee():
    """Get all the employees for employe
    add and remove employees
    """

    form = AddEmployee()
    if request.method == 'POST':
        if form.validate_on_submit():
            add_employees = requests.post(
                "http://{}/employee".format(configuration["API_TEST_HOST"]),
                json={
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "email": form.email.data,
                    "employer_id": app_layout()[0]["_id"]
                }
            )
        return redirect(url_for('dash.employers_employee'))

    employees_req = requests.get(
        "http://{}/employer/{}/employee".format(
            configuration["API_TEST_HOST"],
            current_user.get_id())
    )

    employees = employees_req.json()

    return render_template(
        'employees.html',
        title="Employees",
        current_date=time_date()[0],
        user=app_layout()[0],
        count=app_layout()[1],
        workers=employees["{}".format(app_layout()[1])],
        form=form)


@dash.route('/deleteworker/<id>', strict_slashes=False, methods=["POST"])
@login_required
def delete_worker(id):
    """Detete worker
    """
    del_req = requests.delete(
        "http://{}/employer/{}/employee/{}".format(
            configuration["API_TEST_HOST"],
            current_user.get_id(),
            id
        )
    )

    col_calendar.delete_many({"employee_id": id})

    return redirect(url_for('dash.employers_employee'))


@dash.route('/deleteboss', strict_slashes=False, methods=["POST"])
@login_required
def delete_boss():
    """Detete boss(Main User)
    """

    col_employer.delete_one({"email": app_layout()[0]["email"]})

    flash("Sorry to see you Go!", 'flash-bye')
    return redirect(url_for('auth.logout'))


@dash.route('/profile', strict_slashes=False, methods=['GET', "POST"])
@login_required
def profile():
    """Get all the employees for employe
    add and remove employees
    """

    form = ChangepwdForm()

    if request.method == "POST":
        if form.validate_on_submit():

            if check_pwd(form.password.data, app_layout()[0]["password"]):
                flash('Password used already', 'flash-error')
                return redirect(url_for('dash.profile'))

            req = col_employer.update_one(
                {"email": app_layout()[0]["email"]},
                {"$set": {"password": hash_pwd(form.password.data)}})
            flash('Password successfully Changed!', 'flash-success')
            return redirect(url_for('dash.profile'))

    return render_template(
        'profile_info.html',
        title="Profile",
        current_date=time_date()[0],
        user=app_layout()[0],
        count=app_layout()[1],
        form=form)
