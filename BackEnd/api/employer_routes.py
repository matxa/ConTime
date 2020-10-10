#!/usr/bin/env python3
"""Employer API
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
from models.employer import Employer


"""read from config file"""
with open(os.path.join(sys.path[0], 'config.json')) as conf:
    configuration = json.load(conf)

"""MongoDB setup"""
client = pymongo.MongoClient(configuration["MONGO_URI"])
db = client["ConTime"]
col_employer = db["Employers"]
col_employee = db["Employees"]


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/', methods=["GET"], strict_slashes=False)
def api_home():
    """API Totality or summary,
    API description
    """
    with open(os.path.join(sys.path[0], 'api/api_doc.json')) as doc:
        documentation = json.load(doc)
    return jsonify(documentation)


@api.route('/employer', methods=["GET"], strict_slashes=False)
def get_all_employers():
    """Get all employers
    """
    dictionary_of_employers = []
    employers = col_employer.find()

    for document in employers:
        del document['_id']
        dictionary_of_employers.append(document)

    return jsonify(dictionary_of_employers)


@api.route('/employer', methods=["POST"], strict_slashes=False)
def add_employer():
    """add one employer
    """
    try:
        credentials = request.json
        if credentials is not None:
            if "first_name" in credentials.keys() and "last_name" in\
             credentials.keys() and "email" in credentials.keys():
                new_employer = Employer(
                    credentials["first_name"],
                    credentials['last_name'],
                    credentials['email']
                )
                try:
                    col_employer.create_index("email", unique=True)
                    generated_id = col_employer.insert_one(
                        new_employer.object()).inserted_id
                    return redirect(
                        url_for('api.get_employer_by_id', id=generated_id))
                except Exception:
                    return jsonify({"error": "email already in use"})
            else:
                return jsonify({"error": "missing params to initialize user"})
        else:
            return jsonify({"error": "invalid JSON"})
    except Exception:
        return jsonify({"error": "invalid JSON"})


@api.route('/employer/<id>', methods=["GET"], strict_slashes=False)
def get_employer_by_id(id):
    """get employer
    by id
    """
    try:
        employer = col_employer.find_one({"_id": ObjectId(id)})
        if employer is None:
            return jsonify({"error": "Invalid Employer User ID"})
        else:
            employer = dict(employer)
            del employer['_id']
            return jsonify(employer)
    except Exception as e:
        return jsonify({"error": str(e)})


@api.route(
    '/employer/<id>/employee',
    methods=["GET"],
    strict_slashes=False)
def get_all_employees(id):
    """Get a list of the
    employees the Employer has
    """
    try:
        employer = col_employer.find_one({"_id": ObjectId(id)})
        if employer is None:
            return jsonify({"error": "Invalid Employer User ID"})
        else:
            list_of_employees = []
            employees = col_employee.find({"employer_id": id})
            for document in employees:
                del document['_id']
                list_of_employees.append(document)
            return jsonify({len(list_of_employees): list_of_employees})
    except Exception as e:
        return jsonify({"error": str(e)})


@api.route(
    '/employer/<id>/employee/<employee_id>',
    methods=["GET"],
    strict_slashes=False)
def get_employee(id, employee_id):
    """get/delete employee by id
    """
    try:
        employer = col_employer.find_one({"_id": ObjectId(id)})
        if employer is None:
            return jsonify({"error": "Invalid Employer User ID"})
        else:
            get_employee = col_employee.find_one(
                {"_id": ObjectId(employee_id)})
            if get_employee is None:
                return jsonify({"error": "employee doesn't exist"})
            else:
                get_employee = dict(get_employee)
                del get_employee['_id']
                return jsonify(get_employee)
    except Exception as e:
        return jsonify({"error": str(e)})


@api.route(
    '/employer/<id>/employee/<employee_id>',
    methods=["DELETE"],
    strict_slashes=False)
def delete_employee(id, employee_id):
    """get/delete employee by id
    """
    try:
        employer = col_employer.find_one({"_id": ObjectId(id)})
        if employer is None:
            return jsonify({"error": "Invalid Employer User ID"})
        else:
            get_employee = col_employee.find_one(
                {"_id": ObjectId(employee_id)})
            if get_employee is None:
                return jsonify({"error": "employee doesn't exist"})
            else:
                employees = col_employee.delete_one(
                    {"_id": ObjectId(employee_id)})
                return jsonify(
                    {"message": "Employee {} has been deleted".format(
                        employee_id)})
    except Exception as e:
        return jsonify({"error": str(e)})
