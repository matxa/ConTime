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
from models.utils import (
    time_date,
    hash_pwd,
    check_pwd)
from models.forms import AddEmployee, ChangepwdForm, DaysOfWeek
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
col_employee = db["Employees"]
col_calendar = db["Calendar"]


dash = Blueprint('dash', __name__)


def app_layout():
    """info needed for app
    layout to stay consistent
    """
    """user"""
    req = requests.get(
        "http://{}/employee/{}".format(
            configuration["API_TEST_HOST"], current_user.get_id())
    )
    req_data = req.json()

    employer = requests.get(
        "http://{}/employee/{}/employer".format(
            configuration["API_TEST_HOST"], current_user.get_id())
    )
    employer_data = employer.json()

    return (req_data, employer_data)


@dash.route('/dashboard', strict_slashes=False, methods=['GET', "POST"])
@login_required
def dashboard():
    """dashBoard
    """
    time_dt = time_date()

    form = DaysOfWeek()
    form.sunday = time_dt[1]
    form.employee_id = app_layout()[0]["_id"]
    form.employer_id = app_layout()[0]["employer_id"]

    if request.method == "POST":
        if form.validate_on_submit():
            current_cal = col_calendar.find_one({"week_id": form.week_id()})
            if current_cal is None:
                col_calendar.insert_one(form.object())
                return redirect(url_for('dash.dashboard'))
            else:
                col_calendar.update_one(
                    {"week_id": form.week_id()},
                    {"$set": {"week": form.week()}})
                col_calendar.update_one(
                    {"week_id": form.week_id()},
                    {"$set": {"total_hours": form.total_hours()}})
                return redirect(url_for('dash.dashboard'))

    current_cal = col_calendar.find_one({"week_id": form.week_id()})
    if current_cal is not None:
        this_week = current_cal["week"]
        # SUN
        form.SUN_HOUR.default = this_week[0]["SUN_HOUR"]
        form.SUN_LOCAL.default = this_week[0]["SUN_LOCATION"]
        form.SUN_DESCRIPTION.default = this_week[0]["SUN_DESCRIPTION"]
        # MON
        form.MON_HOUR.default = this_week[1]["MON_HOUR"]
        form.MON_LOCAL.default = this_week[1]["MON_LOCATION"]
        form.MON_DESCRIPTION.default = this_week[1]["MON_DESCRIPTION"]
        # TUE
        form.TUE_HOUR.default = this_week[2]["TUE_HOUR"]
        form.TUE_LOCAL.default = this_week[2]["TUE_LOCATION"]
        form.TUE_DESCRIPTION.default = this_week[2]["TUE_DESCRIPTION"]
        # WED
        form.WED_HOUR.default = this_week[3]["WED_HOUR"]
        form.WED_LOCAL.default = this_week[3]["WED_LOCATION"]
        form.WED_DESCRIPTION.default = this_week[3]["WED_DESCRIPTION"]
        # THU
        form.THU_HOUR.default = this_week[4]["THU_HOUR"]
        form.THU_LOCAL.default = this_week[4]["THU_LOCATION"]
        form.THU_DESCRIPTION.default = this_week[4]["THU_DESCRIPTION"]
        # FRI
        form.FRI_HOUR.default = this_week[5]["FRI_HOUR"]
        form.FRI_LOCAL.default = this_week[5]["FRI_LOCATION"]
        form.FRI_DESCRIPTION.default = this_week[5]["FRI_DESCRIPTION"]
        # SAT
        form.SAT_HOUR.default = this_week[6]["SAT_HOUR"]
        form.SAT_LOCAL.default = this_week[6]["SAT_LOCATION"]
        form.SAT_DESCRIPTION.default = this_week[6]["SAT_DESCRIPTION"]
        form.process()

    return render_template(
        'employeecalendar.html',
        title="Celendar",
        current_date=time_dt[0],
        user=app_layout()[0],
        employer=app_layout()[1],
        form=form,
        week_start_end=time_dt[2])


@dash.route('/pastcalendars', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def past_calendars():
    """get all past calendars
    """

    time_dt = time_date()

    past_cal = col_calendar.find({"employee_id": current_user.get_id()})

    return render_template(
        'pastcalendars.html',
        title="Past Celendars",
        current_date=time_dt[0],
        user=app_layout()[0],
        employer=app_layout()[1],
        past_calendars=past_cal)
