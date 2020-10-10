#!/usr/bin/python3
"""Everything necessary to create
a new employee object
"""
from datetime import datetime
import os
import json
from flask import jsonify
from datetime import datetime
from models.base_user import BaseUser


class Employee(BaseUser):
    """Employee class
    """
    employer_id = ""
