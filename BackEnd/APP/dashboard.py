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
from models.utils import today_date
import requests


dash = Blueprint('dash', __name__)


@dash.route('/dashboard', strict_slashes=False, methods=['GET', "POST"])
@login_required
def dashboard():
    """dashBoard
    """

    """user"""
    req = requests.get(
        "http://192.168.1.8:5050/api/employer/{}".format(current_user.get_id())
    )
    req_data = req.json()
    del req_data["password"]

    """employee count"""
    employee_count = requests.get(
        "http://192.168.1.8:5050/api/employer/{}/employee".format(
            current_user.get_id())
    )
    count = next(iter(employee_count.json()))

    return render_template(
        'appLayout.html',
        user=req_data,
        current_date=today_date(),
        count=count)
