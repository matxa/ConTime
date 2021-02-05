"""EMPLOYEE BLUEPRINT"""
from flask import (
    Blueprint,
    url_for,
    redirect,
    abort,
    render_template,
    jsonify,
    request)
from flask_login import login_required, current_user
from forms import Calendar
from utils import check_user_type
import requests


employee = Blueprint('employee', __name__)

"""API URL"""
# url = "https://api.contime.work"
url = "http://127.0.0.1:5001"


@employee.route('/', strict_slashes=False)
@login_required
def dashboard():
    if check_user_type(current_user.id) != 'employee':
        abort(401)

    """Get current user from API"""
    employee = requests.get(f"{url}/employees/{current_user.id}")

    """Employee job offers"""
    pending_requests = employee.json()['pending_requests']
    company_offers = []
    for company_id in pending_requests:
        company = requests.get(f"{url}/companies/{company_id}")
        company_offers.append(company.json())

    """companies employee work for"""
    companies_work = requests.get(
        f"{url}/employees/{current_user.id}/companies")
    companies = companies_work.json()[1:]

    return render_template(
        'employee_dashboard.html',
        title='Dashboard', company_offers=company_offers, companies=companies)


@employee.route(
    '/job_offer/<company_id>/<status>',
    strict_slashes=False, methods=['POST'])
@login_required
def job_offer(company_id, status):
    """DECLINE JOB REQUEST"""
    if check_user_type(current_user.id) != 'employee':
        abort(401)

    if request.method == 'POST':
        job_decline_url = f"{url}/employees/\
{current_user.id}/companies?company_id={company_id}&status=decline"
        job_accept_url = f"{url}/employees/\
{current_user.id}/companies?company_id={company_id}&status=accept"

        if status == 'decline':
            decline_job = requests.put(job_decline_url)
        if status == 'accept':
            accept_job = requests.put(job_accept_url)

    return redirect(url_for('employee.dashboard'))


@employee.route(
    '/delete_job/<company_id>',
    strict_slashes=False, methods=['POST'])
@login_required
def delete_job(company_id):
    """DECLINE JOB REQUEST"""
    if check_user_type(current_user.id) != 'employee':
        abort(401)

    if request.method == 'POST':
        job_delete_url = f"{url}/employees/\
{current_user.id}/companies?company_id={company_id}"

        delete_job = requests.delete(job_delete_url)

    return redirect(url_for('employee.dashboard'))


@employee.route(
    '/company_calendars/<company_id>',
    strict_slashes=False, methods=['GET', 'POST'])
@login_required
def company_calendars(company_id):
    """Employee calendars given company_id"""
    if check_user_type(current_user.id) != 'employee':
        abort(401)
    """Current calendar"""
    current_calendar = requests.put(f"{url}/calendars/companies/\
{company_id}/employees/{current_user.id}/current")

    """All of employees calendar for company"""
    company_calendars = requests.get(f"{url}/calendars/companies/\
{company_id}/employees/{current_user.id}")

    form = Calendar()

    current_calendar = company_calendars.json()[1]['data'][-1]

    if request.method == 'POST':
        """Current calendar"""
        print(form.schema())
        if form.validate_on_submit:
            update_current_calendar = requests.put(
                f"{url}/calendars/companies/{company_id}/employees/\
{current_user.id}/current", json=form.schema())

        print(update_current_calendar.json())
        return redirect(
            url_for('employee.company_calendars', company_id=company_id))

    # SUN
    form.SUN_HOUR.default = current_calendar['sunday']['hours']
    form.SUN_LOCAL.default = current_calendar['sunday']['location']
    form.SUN_DESCRIPTION.default = current_calendar['sunday']['description']
    # MON
    form.MON_HOUR.default = current_calendar['monday']['hours']
    form.MON_LOCAL.default = current_calendar['monday']['location']
    form.MON_DESCRIPTION.default = current_calendar['monday']['description']
    # TUE
    form.TUE_HOUR.default = current_calendar['tuesday']['hours']
    form.TUE_LOCAL.default = current_calendar['tuesday']['location']
    form.TUE_DESCRIPTION.default = current_calendar['tuesday']['description']
    # WED
    form.WED_HOUR.default = current_calendar['wednesday']['hours']
    form.WED_LOCAL.default = current_calendar['wednesday']['location']
    form.WED_DESCRIPTION.default = current_calendar['wednesday']['description']
    # THU
    form.THU_HOUR.default = current_calendar['thursday']['hours']
    form.THU_LOCAL.default = current_calendar['thursday']['location']
    form.THU_DESCRIPTION.default = current_calendar['thursday']['description']
    # FRI
    form.FRI_HOUR.default = current_calendar['friday']['hours']
    form.FRI_LOCAL.default = current_calendar['friday']['location']
    form.FRI_DESCRIPTION.default = current_calendar['friday']['description']
    # SAT
    form.SAT_HOUR.default = current_calendar['saturday']['hours']
    form.SAT_LOCAL.default = current_calendar['saturday']['location']
    form.SAT_DESCRIPTION.default = current_calendar['saturday']['description']
    form.process()

    calendars = company_calendars.json()[1]['data'][:-1]
    last_calendar = company_calendars.json()[1]['data'].pop()

    return render_template(
        'employee_company_calendar.html',
        form=form, calendars=calendars, company_id=company_id)
