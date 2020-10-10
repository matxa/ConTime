#!/usr/bin/env python3
"""Everything necessary to create
a new employee object
"""
import os
import json
from flask import jsonify
from datetime import datetime
from models.base_user import BaseUser


class Employer(BaseUser):
    """GET data from form and
    save user to datadase
    """
    company_name = ""
    employees = []

    def add_employee(self):
        """add employee
        """
        pass
