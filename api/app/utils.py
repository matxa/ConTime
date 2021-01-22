
"""Utility functions && Common SCHEMAs ⬇
   ▪️ CHANGE_PWD_SCHEMA
   ▪️ company_links()
   ▪️ employee_links()
   ▪️ calendar_links()
   ▪️ code_message()
   ▪️ company_to_json()
   ▪️ employee_to_json()
   ▪️ calendar_to_json()
   ▪️ time_date()
"""
from flask import jsonify
import os
import requests
from datetime import date, timedelta
from dateutil.parser import parse


CHANGE_PWD_SCHEMA = {
    "type" : "object",
    "properties" : {
        "password" : {"type" : "string"}
    },
    "required": [
        "password"
    ]
}


def company_links(id):
    """ add links to company collection """
    links = [
        {
            "rel": "employees",
            "href": f"https://api.contime.work/companies/{id}/employees",
            "action": "GET"
        },
        {
            "rel": "employees",
            "href": f"https://api.contime.work/companies/{id}/employees",
            "action": "PUT",
            "query": {
                "employee_id": {"type" : "string"}
            }
        },
        {
            "rel": "employees",
            "href": f"https://api.contime.work/companies/{id}/employees",
            "action": "DELETE",
            "query": {
                "employee_id": {"type" : "string"}
            }
        },
        {
            "rel": "calendars",
            "href": f"https://api.contime.work/calendars/companies/{id}",
            "action": "GET"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/companies/{id}",
            "action": "GET"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/companies/{id}",
            "action": "PUT"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/companies/{id}",
            "action": "DELETE"
        }
    ]
    return links


def employee_links(id):
    """ add links to employee collection """
    links = [
        {
            "rel": "companies",
            "href": f"https://api.contime.work/employees/{id}/companies",
            "action": "GET"
        },
        {
            "rel": "companies",
            "href": f"https://api.contime.work/employees/{id}/companies",
            "action": "PUT",
            "query": {"company_id": {"type" : "string"}}
        },
        {
            "rel": "companies",
            "href": f"https://api.contime.work/employees/{id}/companies",
            "action": "DELETE",
            "query": {"company_id": {"type" : "string"}}
        },
        {
            "rel": "calendars",
            "href": f"https://api.contime.work/calendars/employees/{id}",
            "action": "GET"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/employees/{id}",
            "action": "GET"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/employees/{id}",
            "action": "PUT"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/employees/{id}",
            "action": "DELETE"
        }
    ]
    return links


def calendar_links(id, employee_id, company_id):
    """ add links to calendar collection """
    links = [
        {
            "rel": "employees",
            "href": f"https://api.contime.work/employees/{employee_id}",
            "action": "GET"
        },
        {
            "rel": "companies",
            "href": f"https://api.contime.work/employees/{company_id}",
            "action": "GET"
        },
        {
            "rel": "self",
            "href": f"https://api.contime.work/calendars/{id}",
            "action": "GET"
        }
    ]
    return links


def code_message(code, message):
    """ exception error message and code """
    return jsonify({ 'code': code, 'message': str(message) }), code

def company_to_json(company):
    """ Take a (company) mongo collection and make json ready """
    company = company.to_mongo()
    company['links'] = company_links(company['_id'])
    company['_id'] = str(company['_id'])
    del company['pending_requests']
    del company['employees']
    del company['date_created']
    del company['password']
    return company


def employee_to_json(employee):
    """ Take a (employee) mongo collection and make json ready """
    employee = employee.to_mongo()
    employee['links'] = employee_links(employee['_id'])
    employee['_id'] = str(employee['_id'])
    del employee['pending_requests']
    del employee['date_created']
    del employee['password']
    del employee['companies']
    return employee


def calendar_to_json(calendar):
    """ Take a (calendar) mongo collection and make json ready """
    calendar = calendar.to_mongo()
    calendar['_id'] = str(calendar['_id'])
    calendar['links'] =  calendar_links(
        calendar["_id"],
        calendar["employee_id"],
        calendar["company_id"])
    del calendar['employee_id']
    del calendar['company_id']
    return calendar


def time_date():
    """Get current date
    ex: Wednesday, October 14
    """
    """make request to time API"""
    req = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")


    dt = parse(req.json()["datetime"])

    """first day of the week == sunday"""
    cur_date = dt.date()
    day_of_week = req.json()["day_of_week"]
    sunday = ""

    if day_of_week < 7:
        sunday = cur_date - timedelta(days=(day_of_week))
    elif day_of_week == 7:
        sunday = cur_date

    days = [str(sunday)]
    for i in range(1, 7):
        days.append(str(sunday + timedelta(days=i)))

    return days

