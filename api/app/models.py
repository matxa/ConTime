"""All models ⬇
[ ▪️ Employee, ▪️ Company, ▪️ Day(EmbeddedDocument), ▪️ Calendar ]
"""
from datetime import datetime
from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField
from mongoengine.fields import (
    ObjectIdField,
    StringField,
    ListField,
    EmailField,
    DateTimeField,
    DecimalField
)
from .utils import time_date


class Employee(Document):
    meta = {'collection': 'employees'}
    companies = ListField()
    pending_requests = ListField()
    first_name = StringField(required=True, max_length=20)
    last_name = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=80)
    date_created = DateTimeField(default=datetime.now)


class Company(Document):
    meta = {'collection': 'companies'}
    company_name = StringField(required=True, max_length=20)
    description = StringField(required=True, max_length=400)
    first_name = StringField(required=True, max_length=20)
    last_name = StringField(required=True, max_length=20)
    email = EmailField(required=True, max_length=50, unique=True)
    password = StringField(required=True, max_length=80)
    employees = ListField()
    pending_requests = ListField()
    date_created = DateTimeField(default=datetime.now)


class Day(EmbeddedDocument):
    day = StringField(default="N/A", max_length=250)
    hours = DecimalField(default=0)
    description = StringField(default="N/A", max_length=250)
    location = StringField(default="N/A", max_length=20)


class Calendar(Document):
    meta = {'collection': 'calendars'}
    time = time_date()
    employee_id = ObjectIdField()
    company_id = ObjectIdField()
    week = StringField(default=time[0])
    total_hours = DecimalField(default=0)
    sunday = EmbeddedDocumentField(Day, default=Day(day=time[0]))
    monday = EmbeddedDocumentField(Day, default=Day(day=time[1]))
    tuesday = EmbeddedDocumentField(Day, default=Day(day=time[2]))
    wednesday = EmbeddedDocumentField(Day, default=Day(day=time[3]))
    thursday = EmbeddedDocumentField(Day, default=Day(day=time[4]))
    friday = EmbeddedDocumentField(Day, default=Day(day=time[5]))
    saturday = EmbeddedDocumentField(Day, default=Day(day=time[6]))
