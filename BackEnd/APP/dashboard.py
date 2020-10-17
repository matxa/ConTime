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
from models.utils import today_date, strip_date
from models.forms import AddEmployee
import requests
import os
import sys
import json


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


dash = Blueprint('dash', __name__)


def app_layout():
    """info needed for app
    layout to stay consistent
    """
    """user"""
    req = requests.get(
        "http://{}/api/employer/{}".format(
            configuration["TEST_HOST"], current_user.get_id())
    )
    req_data = req.json()
    del req_data["password"]

    """employee count"""
    employee_count = requests.get(
        "http://{}/api/employer/{}/employee".format(
            configuration["TEST_HOST"],
            current_user.get_id())
    )
    count = next(iter(employee_count.json()))

    return (req_data, count)


@dash.route('/dashboard', strict_slashes=False, methods=['GET', "POST"])
@login_required
def dashboard():
    """dashBoard
    """

    return render_template(
        'dashboard.html',
        current_date=today_date(),
        user=app_layout()[0],
        count=app_layout()[1])


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
                "http://{}/api/employee".format(configuration["TEST_HOST"]),
                json={
                    "first_name": form.first_name.data,
                    "last_name": form.last_name.data,
                    "email": form.email.data,
                    "employer_id": app_layout()[0]["_id"]
                }
            )
        return redirect(url_for('dash.employers_employee'))

    employees_req = requests.get(
        "http://{}/api/employer/{}/employee".format(
            configuration["TEST_HOST"],
            current_user.get_id())
    )

    employees = employees_req.json()
    
    return render_template(
        'employees.html',
        current_date=today_date(),
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
        "http://{}/api/employer/{}/employee/{}".format(
            configuration["TEST_HOST"],
            current_user.get_id(),
            id
        )
    )

    return redirect(url_for('dash.employers_employee'))


@dash.route('/profile', strict_slashes=False, methods=['GET', "POST"])
@login_required
def profile():
    """Get all the employees for employe
    add and remove employees
    """
    
    return render_template(
        'profile_info.html',
        current_date=today_date(),
        user=app_layout()[0],
        count=app_layout()[1])