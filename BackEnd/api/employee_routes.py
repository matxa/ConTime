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
from api.employer_routes import api
from api.api_errors import api_error


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)

"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]
col_employee = db["Employees"]


@api.route('/employee', methods=["GET"], strict_slashes=False)
def get_employees():
    """get all employees in DataBase
    """
    dictionary_of_employees = []
    employees = col_employee.find()

    for document in employees:
        del document['_id']
        dictionary_of_employees.append(document)

    return jsonify(dictionary_of_employees)


@api.route('/employee', methods=["POST"], strict_slashes=False)
def add_employee():
    """add one employee
    """
    try:
        credentials = request.json
        if credentials is not None:
            if "first_name" in credentials.keys() and "last_name" in\
             credentials.keys() and "email" in credentials.keys() and\
             "employer_id" in credentials.keys():
                new_employee = Employee(
                    credentials["first_name"],
                    credentials['last_name'],
                    credentials['email']
                )
                try:
                    employer = col_employer.find_one({"_id": ObjectId(
                        credentials["employer_id"])})
                    if employer is None:
                        return jsonify(api_error["INVALID_BOSS_ID"])
                    else:
                        try:
                            em = new_employee.object()
                            em["employer_id"] = credentials["employer_id"]
                            check_em = col_employee.find_one({
                                "email": em["email"],
                                "employer_id": em["employer_id"]})
                            if check_em is not None:
                                if check_em is not None:
                                    error = eval(api_error["WORK_ALREADY"])
                                    return jsonify(error)
                                else:
                                    g_id = col_employee.insert_one(
                                        em).inserted_id
                                return redirect(
                                    url_for('api.get_employee_by_id', id=g_id))
                            else:
                                g_id = col_employee.insert_one(
                                    em).inserted_id
                                return redirect(
                                    url_for('api.get_employee_by_id', id=g_id))
                        except Exception as e:
                            return jsonify(api_error["EMAIL_IN_USE"])
                except Exception as e:
                    return jsonify(eval(api_error["EXCEPT_ERR"]))
            else:
                return jsonify(api_error["MISSING_PARAMS"])
        else:
            return jsonify(api_error["INVALID_JSON"])
    except Exception:
        return jsonify(api_error["INVALID_JSON"])


@api.route('/employee/<id>', methods=["GET"], strict_slashes=False)
def get_employee_by_id(id):
    """get employee
    by id
    """
    try:
        employee = col_employee.find_one({"_id": ObjectId(id)})
        if employee is None:
            return jsonify(api_error["INVALID_WORKER"])
        else:
            employee = dict(employee)
            del employee['_id']
            return jsonify(employee)
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))


@api.route('/employee/<id>/employer', methods=["GET"], strict_slashes=False)
def get_employee_employer(id):
    """get the employer of
    given employee by employee id
    """
    try:
        employee = col_employee.find_one({"_id": ObjectId(id)})
        if employee is None:
            return jsonify(api_error["INVALID_WORKER"])
        else:
            employer = col_employer.find_one(
                {"_id": ObjectId(employee["employer_id"])})
            employer = dict(employer)
            del employer["_id"]
            return jsonify(employer)
    except Exception as e:
        return jsonify(eval(api_error['EXCEPT_ERR']))
