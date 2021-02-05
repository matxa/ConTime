"""Companies endpoint
    ▪️ /calendars -> get all calendars
    ▪️ /calendars/{id} -> get calendar by id
    ▪️ /calendars/employees/{employee_id} -> get all employee calendars
    ▪️ /calendars/companies/{company_id} -> get all company calendars
    ▪️ calendars/companies/<company_id>/employees/<employee_id> ⬇
                                        employee-&-company calendars
    ▪️ calendars/companies/<company_id>/employees/<employee_id>/current ⬇
                                                        Current week calendar
"""
import bcrypt
from flask import Blueprint, jsonify, request
from .models import Company, Employee, Calendar
from .utils import (
    code_message,
    company_to_json,
    employee_to_json,
    calendar_to_json,
    CHANGE_PWD_SCHEMA,
    time_date)
from bson import ObjectId
from jsonschema import validate
from mongoengine.errors import DoesNotExist

DAY_REF = {
    "type": "object",
    "properties": {
        "hours": {"type": "number"},
        "description": {"type": "string"},
        "location": {"type": "string"},
    },
    "required": [
        "hours",
        "description",
        "location",
    ]
}
CALENDAR_SCHEMA = {
    "type": "object",
    "properties": {
        "sunday": DAY_REF,
        "monday": DAY_REF,
        "tuesday": DAY_REF,
        "wednesday": DAY_REF,
        "thursday": DAY_REF,
        "friday": DAY_REF,
        "saturday": DAY_REF,
    },
    "required": [
        "sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
    ]
}


""" Companies Blueprint"""
calendars = Blueprint('calendars', __name__)


@calendars.route('/', strict_slashes=False)
def all_calendars():
    """Return all the calendars from the database"""
    _calendars = Calendar.objects()
    __calendars = []
    for calendar in _calendars:
        calendar = calendar_to_json(calendar)
        __calendars.append(calendar)
    return jsonify([
        {
            "metadata": {"count": len(_calendars)},
            "links": [
                {
                    "rel": "self",
                    "href": f"https://api.contime.work/calendars",
                    "action": "GET",
                },
            ]
        },
        {
            "data": __calendars
        },
    ])


@calendars.route('/<id>', strict_slashes=False)
def calendar_by_id(id):
    """return calendar by id"""
    try:
        calendar = Calendar.objects.get(id=ObjectId(id))
        calendar = calendar_to_json(calendar)
        return jsonify(calendar), 200
    except Exception as e:
        return code_message(404, e)


@calendars.route('/employees/<employee_id>', strict_slashes=False)
def employee_calendars(employee_id):
    """Return all employees calendar"""
    try:
        _calendars = Calendar.objects(employee_id=employee_id)
        __calendars = []
        for calendar in _calendars:
            calendar = calendar_to_json(calendar)
            __calendars.append(calendar)
        return jsonify([
            {
                "metadata": {"count": len(_calendars)},
            },
            {
                "data": __calendars
            },
        ])
    except Exception as e:
        return code_message(400, e)


@calendars.route('/companies/<company_id>', strict_slashes=False)
def company_calendars(company_id):
    """Return all employees calendar"""
    try:
        _calendars = Calendar.objects(company_id=company_id)
        __calendars = []
        for calendar in _calendars:
            calendar = calendar_to_json(calendar)
            __calendars.append(calendar)
        return jsonify([
            {
                "metadata": {"count": len(_calendars)},
            },
            {
                "data": __calendars
            },
        ]), 200
    except Exception as e:
        return code_message(400, e)


@calendars.route(
    '/companies/<company_id>/employees/<employee_id>', strict_slashes=False)
def company_employee_calendars(company_id, employee_id):
    """Return All calendars where employee_id
    and company_id present
    """
    try:
        _calendars = Calendar.objects(
            company_id=company_id, employee_id=employee_id)
        __calendars = []
        for calendar in _calendars:
            calendar = calendar_to_json(calendar)
            __calendars.append(calendar)
        return jsonify([
            {
                "metadata": {"count": len(_calendars)},
            },
            {
                "data": __calendars
            },
        ]), 200
    except Exception as e:
        return code_message(400, e)


@calendars.route(
    '/companies/<company_id>/employees/<employee_id>/current',
    strict_slashes=False, methods=['PUT'])
def current_calendar(company_id, employee_id):
    """Current week calendar"""
    try:
        time = time_date()
        curr_calendar = Calendar.objects.get(
            company_id=company_id,
            employee_id=employee_id,
            week=time[0]
        )
        try:
            validate(instance=request.json, schema=CALENDAR_SCHEMA)
        except Exception as e:
            return code_message(400, str(e).split('\n')[0])
        request.json['sunday']['day'] = time[0]
        request.json['monday']['day'] = time[1]
        request.json['tuesday']['day'] = time[2]
        request.json['wednesday']['day'] = time[3]
        request.json['thursday']['day'] = time[4]
        request.json['friday']['day'] = time[5]
        request.json['saturday']['day'] = time[6]
        total_hours = request.json['sunday']['hours'] +\
            request.json['monday']['hours'] +\
            request.json['tuesday']['hours'] +\
            request.json['wednesday']['hours'] +\
            request.json['thursday']['hours'] +\
            request.json['friday']['hours'] +\
            request.json['saturday']['hours']
        request.json['total_hours'] = total_hours
        curr_calendar.modify(**request.json)
        curr_calendar = calendar_to_json(curr_calendar)
        return jsonify(curr_calendar), 200
    except DoesNotExist:
        new_calendar = Calendar(
            company_id=company_id,
            employee_id=employee_id,
            week=time[0])
        new_calendar.save()
        new_calendar = calendar_to_json(new_calendar)
        return jsonify(new_calendar), 201
