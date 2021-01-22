"""Companies endpoint
    ▪️ /companies -> [ GET, POST ]
    ▪️ /companies/{ id } -> [ GET, PUT, DELETE ]
    ▪️ /companies/{ id }/employees -> [ GET, PUT, DELETE ]
"""
import bcrypt
from flask import Blueprint, jsonify, request
from .models import Company, Employee
from .utils import (
    code_message,
    company_to_json,
    employee_to_json,
    CHANGE_PWD_SCHEMA)
from bson import ObjectId
from jsonschema import validate


COMPANY_SCHEMA = {
    "type" : "object",
    "properties" : {
        "first_name" : {"type" : "string"},
        "last_name" : {"type" : "string"},
        "email" : {"type" : "string"},
        "password" : {"type" : "string"},
        "company_name" : {"type" : "string"},
        "description" : {"type" : "string"},
        "date_created": {"type" : "string"},
    },
    "required": [
        "first_name",
        "last_name",
        "email",
        "password",
        "company_name",
        "description"
    ]
}


""" Companies Blueprint"""
companies = Blueprint('companies', __name__)


@companies.route('/', methods=['GET', 'POST'], strict_slashes=False)
def all_companies():
    """ return a list of companies in the database
    create a new company.
    """
    _companies = Company.objects()
    if request.method == 'GET':
        __companies = []
        for company in _companies:
            company = company_to_json(company)
            __companies.append(company)
        return jsonify([
            {
                "metadata": { "count": len(_companies) },
                "links": [
                    {
                        "rel": "self",
                        "href": f"https://api.contime.work/companies",
                        "action": "GET",
                    },
                    {
                        "rel": "self",
                        "href": f"https://api.contime.work/companies",
                        "action": "POST",
                        "schema" : {
                            "first_name" : {"type" : "string"},
                            "last_name" : {"type" : "string"},
                            "email" : {"type" : "string"},
                            "password" : {"type" : "string"},
                            "company_name" : {"type" : "string"},
                            "description" : {"type" : "string"},
                            "date_created": {"type" : "string"},
                        }
                    },
                ]
            },
            {
                "data": __companies
            }
        ]
        ), 200

    if request.method == 'POST':
        try:
            validate(instance=request.json, schema=COMPANY_SCHEMA)
            new_company = Company(**request.json)
            new_company.password = bcrypt.hashpw(
                request.json['password'].encode(encoding='UTF-8'),
                bcrypt.gensalt()).__str__()
            new_company.save()
            new_company = company_to_json(new_company)
            return jsonify(new_company), 201
        except Exception as e:
            return code_message(400, str(e).split('\n')[0])


@companies.route('/<id>', methods=['GET','PUT','DELETE'], strict_slashes=False)
def company(id):
    """ obtain / modify company by id """
    try:
        company = Company.objects.get(id=ObjectId(id))
    except Exception as e:
        return code_message(404, e)
    if request.method == 'GET':
        company = company_to_json(company)
        return jsonify(company), 200
    if request.method == 'PUT':
        try:
            validate(instance=request.json, schema=CHANGE_PWD_SCHEMA)
            company.password = bcrypt.hashpw(
                request.json['password'].encode(encoding='UTF-8'),
                bcrypt.gensalt()).__str__()
            company.save()
            company = company_to_json(company)
            return jsonify(company), 200
        except Exception as e:
            return code_message(400, str(e).split('\n')[0])
    if request.method == 'DELETE':
        company.delete()
        return code_message(204, "No Content")


@companies.route(
    '/<id>/employees',
    methods=['GET', 'PUT', 'DELETE'],strict_slashes=False)
def employees(id):
    """Return list of company employees
    Request employee to work for company
    QUERY params -> employee_id
    """
    try:
        company = Company.objects.get(id=ObjectId(id))
    except Exception as e:
        return code_message(404, e)
    if request.method == 'GET':
        _employees = Employee.objects.filter(companies__contains=company.id)
        __employees = [{ "metadata": { "count": len(_employees) } }]
        for employee in _employees:
            employee = employee_to_json(employee)
            __employees.append(employee)
        return jsonify(__employees)
    if request.method == "PUT":
        if "employee_id" in request.args.keys():
            try:
                employee = Employee.objects.get(
                    id=ObjectId(request.args.get('employee_id')))
                if employee.id not in company.employees and employee.id not\
                   in company.pending_requests:
                    company.pending_requests.append(employee.id)
                    employee.pending_requests.append(company.id)
                    company.save()
                    employee.save()
                    return jsonify({ "request": "successful" }), 200
            except Exception as e:
                return code_message(404, e)
        return jsonify({ "request": "Bad Request" }), 400
    if request.method == "DELETE":
        if "employee_id" in request.args.keys():
            try:
                employee = Employee.objects.get(
                    id=ObjectId(request.args.get('employee_id')))
                if employee.id in company.employees:
                    company.employees.remove(employee.id)
                    employee.companies.remove(company.id)
                    company.save()
                    employee.save()
                    return jsonify({ "request": "successful" }), 200
            except Exception as e:
                return code_message(404, e)
        return jsonify({ "request": "Bad Request" }), 400
