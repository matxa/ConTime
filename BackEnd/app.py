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
    session)

from api.employer_routes import api
from flask_pymongo import PyMongo
from models.employer import Employer
from models.employee import Employee
import os
import json

"""read from config file"""
with open('config.json') as conf:
    configuration = json.load(conf)


"""App configutation"""
app = Flask(__name__)
app.config["SECRET_KEY"] = configuration["FLASK_SECRET_KEY"]
app.config["MONGO_URI"] = configuration["MONGO_URI"]
mongo = PyMongo(app)


"""Register Blueprints to app"""
app.register_blueprint(api)

if __name__ == "__main__":
    app.run(
        debug=True)
