"""COMPANY BLUEPRINT"""
from flask import (
    Blueprint,
    url_for,
    redirect,
    abort,
    render_template,
    jsonify,
    request,
    flash)
from flask_login import login_required, current_user, logout_user
from forms import Calendar, Password, Email
from utils import check_user_type
import requests


company = Blueprint('company', __name__)


"""API URL"""
# url = "https://api.contime.work"
url = "http://127.0.0.1:5001"


@company.route('/', strict_slashes=False, methods=['GET', 'POST'])
@login_required
def dashboard():
    """Check is current user is of type company"""
    if check_user_type(current_user.id) != 'company':
        abort(401)

    form = Email()

    """Get current user from API"""
    company = requests.get(f"{url}/companies/{current_user.id}")

    """Employees working for company"""
    employees_work = requests.get(
        f"{url}/companies/{current_user.id}/employees")
    employees = employees_work.json()[1:]

    if request.method == "POST":
        if form.validate_on_submit():
            _employee = requests.get(
                f"{url}/employee?email={form.email.data}")

            if _employee.status_code == 200:
                employee_id = _employee.json()['employee']['id']
                add_employee = requests.put(
                    f"{url}/companies/{current_user.id}/\
employees?employee_id={employee_id}")
                if add_employee.status_code == 400:
                    flash(
                        "Employee already in company",
                        category='flash-error')
                    return redirect(url_for('company.dashboard'))
                if add_employee.status_code == 200:
                    flash(
                        "Request sent successfully",
                        category='flash-success')
                    return redirect(url_for('company.dashboard'))
            else:
                flash(
                    "Employee doesn't exist",
                    category='flash-error')
                return redirect(url_for('company.dashboard'))

    return render_template(
        'company_dashboard.html', employees=employees, form=form)


@company.route(
    '/employee_calendars/<employee_id>',
    strict_slashes=False)
@login_required
def employee_calendars(employee_id):
    """All of employees calendar for company"""
    if check_user_type(current_user.id) != 'company':
        abort(401)

    if employee_id == 'DELETED':
        return redirect(url_for('company.company_calendars'))

    employee_calendars = requests.get(f"{url}/calendars/companies/\
{current_user.id}/employees/{employee_id}")

    calendars = employee_calendars.json()[1]['data']
    employee = requests.get(f"{url}/employees/{employee_id}")

    return render_template(
        'company_calendars.html', calendars=calendars,
        employee=employee.json())


@company.route('/all_calendars', strict_slashes=False)
@login_required
def company_calendars():
    """All calendars for company"""
    if check_user_type(current_user.id) != 'company':
        abort(401)

    request_calendars = requests.get(
        f'{url}/calendars/companies/{current_user.id}')
    calendars = request_calendars.json()[1]['data']
    for calendar in calendars:
        request_employee = requests.get(calendar['links'][0]['href'])
        if request_employee.status_code == 404:
            calendar['employee_name'] = 'DELETED'
            calendar['employee_id'] = 'DELETED'
        if request_employee.status_code == 200:
            calendar['employee_name'] = request_employee.json()['first_name']\
                + " " + request_employee.json()['last_name']
            calendar['employee_id'] = request_employee.json()['_id']

    return render_template(
        'company_employee_calendar.html', calendars=calendars)


@company.route(
    '/profile',
    strict_slashes=False, methods=['GET', 'POST', 'DELETE'])
@login_required
def profile():
    """Profile"""
    if check_user_type(current_user.id) != 'company':
        abort(401)
    form = Password()

    """Get current user from API"""
    company = requests.get(f"{url}/companies/{current_user.id}")

    if request.method == 'POST':
        if form.validate_on_submit():
            pwd = requests.put(
                f"{url}/companies/{current_user.id}",
                json={'password': form.password.data})
            if pwd.status_code == 200:
                flash(
                    "Password Changed successfully",
                    category='flash-success')
            else:
                flash(
                    "Something Went Wromg",
                    category='flash-error')
        else:
            flash(
                "Passwords don't validate",
                category='flash-error')
        return redirect(url_for('company.profile'))

    return render_template(
        'company_profile.html', form=form, company=company.json())


@company.route(
    '/delete_employee/<employee_id>',
    strict_slashes=False, methods=['POST'])
@login_required
def delete_employee(employee_id):
    """DELETE EMPLOYEE FROM EMPLOYEE's LIST"""
    if check_user_type(current_user.id) != 'company':
        abort(401)

    if request.method == 'POST':
        employee_delete_url = f"{url}/companies/\
{current_user.id}/employees?employee_id={employee_id}"

        delete_employee = requests.delete(employee_delete_url)

    return redirect(url_for('company.dashboard'))


@company.route(
    '/delete_user',
    strict_slashes=False, methods=['POST'])
@login_required
def delete_user():
    """Delete user"""
    if check_user_type(current_user.id) != 'company':
        abort(401)

    if request.method == 'POST':
        delete_user = requests.delete(f"{url}/companies/{current_user.id}")
        if delete_user.status_code == 204:
            logout_user()
            flash(
                "Sad to see you go :(",
                category='flash-error')
            return redirect(url_for('login'))
        return redirect(url_for('company.profile'))
