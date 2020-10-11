#!/usr/bin/python3
"""Everything necessary to create
a new employee object
"""
from datetime import datetime
import os
import json
from flask import jsonify
from datetime import datetime


class BaseUser():
    """GET data from form and
    save user to datadase
    """
    def __init__(self, first_name, last_name, email):
        """define a Employer
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.date_created = datetime.now()

    def object(self):
        """Object used to dump
        in database
        """
        object = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "date_created": self.date_created,
        }

        return object

    def __str__(self):
        """json format of Employee
        instance
        """
        json_str = json.dumps(self.object(), indent=4)
        return json_str
