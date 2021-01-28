""" API Server setup ✅
    ▪️ / -> Home endpoint
    ▪️ /login -> Login endpoint
    ▪️ /employee -> Get employee id using email ..endpoint
"""
from app.company_endpoints import companies
from app.employee_endpoints import employees
from app.calendar_endpoint import calendars
import bcrypt
from flask import Flask, redirect, render_template, request
from flask_mongoengine import MongoEngine
import markdown
import markdown.extensions.fenced_code
from flask import jsonify
from flask_cors import CORS
from os import getenv
from app.utils import code_message
from app.models import Company, Employee, Calendar
from bson import ObjectId


"""Flask App"""
app = Flask(__name__)
CORS(app)
app.register_blueprint(companies, url_prefix="/companies")
app.register_blueprint(employees, url_prefix="/employees")
app.register_blueprint(calendars, url_prefix="/calendars")


"""DATABASE CONNECTION"""
DB_USER = getenv("DB_USER")
DB_PWD = getenv("DB_PWD")
DB_URI = f"mongodb+srv://{DB_USER}:{DB_PWD}@cluster0.qgdv3.mongodb.net/\
ConTime?retryWrites=true&w=majority"

app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine(app)


@app.route("/", strict_slashes=False)
def index():
    """Render markdown"""
    readme_file = open("README.md", "r")
    md_template_string = markdown.markdown(
        readme_file.read(), extensions=["fenced_code"]
    )

    return md_template_string


@app.route("/login", strict_slashes=False)
def login():
    """LogIn User
    QUERY Params ⬇
    email, password, type=( company or employee )
    return user id
    """
    if "email" in request.args.keys() and "password" in request.args.keys()\
       and "type" in request.args.keys():
        if request.args.get('type') == "company":
            try:
                company = Company.objects.get(email=request.args.get('email'))
                company = company.to_mongo()
                if bcrypt.checkpw(
                   request.args.get('password').encode(encoding='UTF-8'),
                   eval(company['password'])):
                    res = {
                        "company": {
                            "id": str(company["_id"]),
                        }
                    }
                    return jsonify(res), 200
            except Exception as e:
                return code_message(404, e)
        elif request.args.get('type') == "employee":
            try:
                employee = Employee.objects.get(
                    email=request.args.get('email'))
                employee = employee.to_mongo()
                if bcrypt.checkpw(
                   request.args.get('password').encode(encoding='UTF-8'),
                   eval(employee['password'])):
                    res = {
                        "employee": {
                            "id": str(employee["_id"])
                        }
                    }
                    return jsonify(res), 200
            except Exception as e:
                return code_message(404, e)

    return code_message(400, "Bad Request")


@app.route("/employee", strict_slashes=False)
def find_employee():
    """find employee using email
    in order to make a request
    QUERY params -> email
    return employee id
    """
    if "email" in request.args.keys():
        try:
            employee = Employee.objects.get(email=request.args.get('email'))
            employee = employee.to_mongo()
            res = {
                "employee": {
                    "id": str(employee["_id"]),
                }
            }
            return jsonify(res), 200
        except Exception as e:
            return code_message(404, e)
    return code_message(400, "missing Query")


if __name__ == '__main__':
    app.run(debug=True)
