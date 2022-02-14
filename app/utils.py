"""UTILS functions"""
import requests
from __init__ import API_URL


def check_user_type(user_id):
    """Employee or Company"""
    user_type = ''
    employee = requests.get(f"{API_URL}/employees/{user_id}")
    company = requests.get(f"{API_URL}/companies/{user_id}")
    if employee.status_code == 200:
        user_type = 'employee'
    if company.status_code == 200:
        user_type = 'company'
    return user_type
