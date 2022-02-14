"""Companies endpoint
    ▪️ /employees -> [ GET, POST ]
    ▪️ /employees/{ id } -> [ GET, PUT, DELETE ]
    ▪️ /employees/{ id }/companies -> [ GET, PUT, DELETE ]
"""
import bcrypt
from flask import Blueprint, jsonify, request
from .models import Employee, Company
from .utils import (
    code_message,
    employee_links,
    employee_to_json,
    company_to_json,
    CHANGE_PWD_SCHEMA)
from bson import ObjectId
from jsonschema import validate
from . import API_URL


EMPLOYEE_SCHEMA = {
    "type": "object",
    "properties": {
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"}
    },
    "required": [
        "first_name",
        "last_name",
        "email",
        "password"
    ]
}


""" Companies Blueprint"""
employees = Blueprint('employees', __name__)


@employees.route('/', methods=['GET', 'POST'], strict_slashes=False)
def all_employees():
    """ return a list of employees in the database
    create a new employee.
    """
    _employees = Employee.objects()
    if request.method == 'GET':
        __employees = []
        for employee in _employees:
            employee = employee_to_json(employee)
            __employees.append(employee)
        return jsonify([
            {
                "metadata": {"count": len(_employees)},
                "links": [
                    {
                        "rel": "self",
                        "href": f"{API_URL}/employees",
                        "action": "GET",
                    },
                    {
                        "rel": "self",
                        "href": f"{API_URL}/employees",
                        "action": "POST",
                        "schema": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "email": {"type": "string"},
                            "password": {"type": "string"}
                        },
                    },
                ]
            },
            {
                "data": __employees
            }
        ]
        ), 200

    if request.method == 'POST':
        try:
            validate(instance=request.json, schema=EMPLOYEE_SCHEMA)
            new_employee = Employee(**request.json)
            new_employee.password = bcrypt.hashpw(
                request.json['password'].encode(encoding='UTF-8'),
                bcrypt.gensalt()).__str__()
            new_employee.save()
            new_employee = employee_to_json(new_employee)
            return jsonify(new_employee), 201
        except Exception as e:
            return code_message(400, str(e).split('\n')[0])


@employees.route(
    '/<id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def company(id):
    """ obtain / modify company by id """
    try:
        employee = Employee.objects.get(id=ObjectId(id))
    except Exception as e:
        return code_message(404, e)
    if request.method == 'GET':
        employee = employee_to_json(employee)
        return jsonify(employee), 200
    if request.method == 'PUT':
        try:
            validate(instance=request.json, schema=CHANGE_PWD_SCHEMA)
            employee.password = bcrypt.hashpw(
                request.json['password'].encode(encoding='UTF-8'),
                bcrypt.gensalt()).__str__()
            employee.save()
            employee = employee_to_json(employee)
            return jsonify(employee), 200
        except Exception as e:
            return code_message(400, str(e).split('\n')[0])
    if request.method == 'DELETE':
        employee.delete()
        return code_message(204, "No Content")


@employees.route(
    '/<id>/companies',
    methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def companies(id):
    """Return list of employees companies
    Request employee to work for company
    QUERY params -> company_id
    """
    try:
        employee = Employee.objects.get(id=ObjectId(id))
    except Exception as e:
        return code_message(404, e)
    if request.method == 'GET':
        _companies = Company.objects.filter(
            employees__contains=employee.id)
        __companies = [{"metadata": {"count": len(_companies)}}]
        for company in _companies:
            company = company_to_json(company)
            __companies.append(company)
        return jsonify(__companies), 200
    if request.method == "PUT":
        if "company_id" in request.args.keys() and\
           "status" in request.args.keys():
            try:
                company = Company.objects.get(
                    id=ObjectId(request.args.get('company_id')))
                """ACCEPT JOB OFFER"""
                if company.id in employee.pending_requests and\
                   company.id not in employee.companies and\
                   request.args['status'] == 'accept':
                    employee.companies.append(company.id)
                    employee.pending_requests.remove(company.id)
                    company.pending_requests.remove(employee.id)
                    company.employees.append(employee.id)
                    employee.save()
                    company.save()
                    return jsonify({"request": "successful"}), 200
                """DECLINE JOB OFFER"""
                if company.id in employee.pending_requests and\
                   company.id not in employee.companies and\
                   request.args['status'] == 'decline':
                    employee.pending_requests.remove(company.id)
                    company.pending_requests.remove(employee.id)
                    employee.save()
                    company.save()
                    return jsonify({"request": "successful"}), 200

                return code_message(400, "Bad request")
            except Exception as e:
                return code_message(404, e)
        return code_message(400, "Bad request")

    if request.method == "DELETE":
        if "company_id" in request.args.keys():
            try:
                company = Company.objects.get(
                    id=ObjectId(request.args.get('company_id')))
                if company.id in employee.companies:
                    employee.companies.remove(company.id)
                    company.employees.remove(employee.id)
                    employee.save()
                    company.save()
                    return jsonify({"request": "successful"}), 200
                return jsonify({"request": "fail"}), 200
            except Exception as e:
                return code_message(404, e)
