#!/usr/bin/env python3
"""ConTime API
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
    flash,
    Blueprint)
from api.employer_routes import employer
from api.employee_routes import employee
from api.calendar_routes import calendar
import os
import sys
import json


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)


"""API APP and BluePrints"""
api = Flask(__name__)
api.register_blueprint(employer)
api.register_blueprint(employee)


"""API Congiguration"""
api.config["SECRET_KEY"] = configuration["FLASK_SECRET_KEY"]
api.secret_key = configuration["FLASK_SECRET_KEY"]
api.config["MONGO_URI"] = configuration["MONGO_URI"]


if __name__ == "__main__":
    api.run(
        host=configuration["API_HOST"],
        port=configuration["API_PORT"],
        debug=True
    )
