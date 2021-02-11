"""FRONTEND APP"""
from flask import (
    Flask, render_template, request,
    jsonify, redirect, flash, session, url_for)
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user)
from company import company
from employee import employee
from forms import Login
from forms import EmployeeRegistration
from forms import CompanyResgistration
import requests
from utils import check_user_type


"""Flask App"""
app = Flask(__name__)
app.config["SECRET_KEY"] = '12345gberwdf4356754refsw'
app.register_blueprint(company, url_prefix='/company')
app.register_blueprint(employee, url_prefix='/employee')

"""API URL"""
url = "https://api.contime.work"


"""USER LOGIN"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please Login!"
login_manager.login_message_category = "flash-error"


class User(UserMixin):
    """User Model"""
    id = ''


@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.id = user_id
    return user


@app.errorhandler(404)
def page_not_found(e):
    """404 ERROR handler"""
    return render_template('404.html'), 404


@app.errorhandler(401)
def page_not_found(e):
    """401 ERROR handler"""
    return render_template('401.html'), 401


@app.route('/', strict_slashes=False)
def home():
    """Landing page of the application"""
    return render_template('landing_page.html')


@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Login"""

    if current_user.is_authenticated:
        return redirect(
            url_for(f'{check_user_type(current_user.id)}.dashboard'))
    form = Login()
    if request.method == 'POST':
        req = requests.get(f'{url}/login?email=\
{form.email.data}&password={form.password.data}&type=\
{form.login_type.data}')
        if req.status_code == 404:
            flash("Account doesn't exist!", category='flash-error')
            return redirect('login')
        if req.status_code == 400:
            flash("Incorrect password!", category='flash-error')
            return redirect('login')

        """Login User"""
        user = User()
        if form.login_type.data == 'employee':
            user.id = req.json()['employee']['id']
            login_user(user)
            return redirect(url_for('employee.dashboard'))
        if form.login_type.data == 'company':
            user.id = req.json()['company']['id']
            login_user(user)
            return redirect(url_for('company.dashboard'))

    return render_template('login.html', title='Login', form=form)


@app.route('/logout', strict_slashes=False)
def logout():
    """Logout user"""
    logout_user()
    flash("Logout successfully!", category='flash-success')
    return redirect('login')


@app.route('/register', methods=['GET', 'POST'], strict_slashes=False)
def register():
    """Register Company or Employee"""
    if current_user.is_authenticated:
        return redirect(
            url_for(f'{check_user_type(current_user.id)}.dashboard'))
    employee_form = EmployeeRegistration()
    company_form = CompanyResgistration()

    if request.method == 'POST':
        """Register employee"""
        if employee_form.validate_on_submit():
            if employee_form.login_type.data == 'employee':
                post_employee = requests.post(
                    f"{url}/employees", json=employee_form.schema())
                if post_employee.status_code == 201:
                    flash(
                        "Account created successfully",
                        category='flash-success')
                    return redirect('login')
                else:
                    flash("Account already in use!", category='flash-error')
            return redirect('register')
        else:
            return redirect('register')

        """Register company"""
        if company_form.validate_on_submit():
            if employee_form.login_type.data == 'company':
                post_company = requests.post(
                    f"{url}/companies", json=company_form.schema())
                if post_company.status_code == 201:
                    flash(
                        "Account created successfully",
                        category='flash-success')
                    return redirect('login')
                else:
                    flash("Account already in use!", category='flash-error')
                return redirect('register')

    return render_template(
        'register.html', title='Register',
        employee_form=employee_form, company_form=company_form)


if __name__ == '__main__':
    app.run()
