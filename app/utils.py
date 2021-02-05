"""UTILS functions"""
import requests

"""API url"""
url = "https://api.contime.work"


def check_user_type(user_id):
    """Employee or Company"""
    user_type = ''
    employee = requests.get(f"{url}/employees/{user_id}")
    company = requests.get(f"{url}/companies/{user_id}")
    if employee.status_code == 200:
        user_type = 'employee'
    if company.status_code == 200:
        user_type = 'company'
    return user_type
