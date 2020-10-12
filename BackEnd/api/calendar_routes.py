#!/usr/bin/env python3
"""Employee API
"""
from flask import (
    Blueprint,
    Flask,
    jsonify,
    request,
    redirect,
    url_for)
import pymongo
import json
import os
import sys
from bson.objectid import ObjectId
from models.employee import Employee
from models.calendar import WeekCalendar, start_end_week
from api.employer_routes import api
from api.api_errors import api_error
import datetime


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)

"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]
col_employee = db["Employees"]
col_calendar = db["Calendar"]


@api.route(
    '/calendar/employee/<employee_id>/',
    methods=["GET"],
    strict_slashes=False)
def get_calendars(employee_id):
    """get all calendars
    for given employees
    """
    try:
        calendar = col_calendar.find({
            "employee_id": employee_id,
        })

        calendars = []
        for cal in calendar:
            del cal["_id"]
            calendars.append(cal)
        return jsonify(calendars)
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))


@api.route(
    '/calendar/<employee_id>/<date>',
    methods=["GET"],
    strict_slashes=False)
def get_employee_calendar(employee_id, date):
    """get week worked
    """
    try:
        calendar = col_calendar.find({
            "employee_id": employee_id,
            "week_start_end": str(start_end_week(
                datetime.datetime.strptime(date, '%Y-%m-%d').date())[0])
        })

        calendars = []
        for cal in calendar:
            del cal["_id"]
            calendars.append(cal)
        return jsonify(calendars)
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))


@api.route(
    '/calendar/<employee_id>/<date>',
    methods=["POST"],
    strict_slashes=False)
def post_employee_calendar(employee_id, date):
    """get the calendar for given employee_id
    """
    try:
        employee = col_employee.find_one({"_id": ObjectId(employee_id)})
        if employee is None:
            return jsonify(api_error["INVALID_WORKER"])
        else:
            calendar_week = WeekCalendar(
                datetime.datetime.strptime(date, '%Y-%m-%d').date(),
                str(employee["_id"]),
                employee["employer_id"])
            col_calendar.create_index("calendar_id", unique=True)

            col_calendar.insert_one(calendar_week.object())
            return redirect(url_for('api.get_employee_calendar',
                            employee_id=employee_id,
                            date=date))
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))


@api.route(
    '/calendar/employer/<employer_id>',
    methods=["GET"],
    strict_slashes=False)
def get_workers_calendars(employer_id):
    """get all the calendars where
    employer_id
    """
    try:
        calendar = col_calendar.find({
            "employer_id": employer_id,
        })

        calendars = []
        for cal in calendar:
            del cal["_id"]
            calendars.append(cal)
        return jsonify(calendars)
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))


@api.route(
    '/calendar/employer/<employer_id>/<date>',
    methods=["GET"],
    strict_slashes=False)
def get_workers_calendars_by_date(employer_id, date):
    """get workers calendar
    by date
    """
    try:
        calendar = col_calendar.find({
            "employer_id": employer_id,
            "week_start_end": str(start_end_week(
                datetime.datetime.strptime(date, '%Y-%m-%d').date())[0])
        })

        calendars = []
        for cal in calendar:
            del cal["_id"]
            calendars.append(cal)
        return jsonify(calendars)
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))
