# ConTime API

![contime_logo](https://i.imgur.com/D6X6mDf.png)

## [ConTime API](https://api.contime.work/) is the bridge between the backend and the frontend of the [ConTime Web Application](https://github.com/matxa/ConTime).
<hr>

&#10240;

### Technologies & Tools used :
- [Python](https://www.python.org/) v3.8.5
    - [Flask](https://flask.palletsprojects.com/en/1.1.x/) - "a micro web framework."
    - [JsonSchema](https://python-jsonschema.readthedocs.io/en/stable/) - "an implementation of JSON Schema for Python."
    - [MongoEngine](http://docs.mongoengine.org/) - "a python object data mapper for mongodb."
    - [Bcrypt](https://pypi.org/project/bcrypt/) - "Good password hashing for your software and your servers."
- [MongoDB](https://www.mongodb.com/1) - "A document database, which means it stores data in JSON-like documents..."

&#10240;

### ConTime API Roles:

- ConTime is a web application that makes it easier for Sub(Contractors) to keep track of their employee's working history.

    - Quick Overview of API features
        - CREATE [ company, employee, calendars ]
        - DELETE [ company, employee ]
        - UPDATE [ company_password, employee_password, send_job_request, weekly_calendar ]

    &#10240; The Roles of the API are better understood in the <i>endpoint section</i>


&#10240;

## &#10240; Schemas &#10240; &#123; &#34; &#34; &#58; &#34; &#34; &#125;

- __Company__
```json
COMPANY_SCHEMA = {
    "type" : "object",
    "properties" : {
        "first_name" : {"type" : "string"},
        "last_name" : {"type" : "string"},
        "email" : {"type" : "string"},
        "password" : {"type" : "string"},
        "company_name" : {"type" : "string"},
        "description" : {"type" : "string"},
    },
    "required": [
        "first_name",
        "last_name",
        "email",
        "password",
        "company_name",
        "description"
    ]
}
```
- __Employee__
```json
EMPLOYEE_SCHEMA = {
    "type" : "object",
    "properties" : {
        "first_name" : {"type" : "string"},
        "last_name" : {"type" : "string"},
        "email" : {"type" : "string"},
        "password" : {"type" : "string"}
    },
    "required": [
        "first_name",
        "last_name",
        "email",
        "password"
    ]
}
```
- __Calendar__
```json
DAY_REF = {
    "type" : "object",
    "properties": {
        "hours": {"type" : "number"},
        "description": {"type" : "string"},
        "location": {"type" : "string"},
    },
    "required": [
        "hours",
        "description",
        "location",
    ]
}
CALENDAR_SCHEMA = {
    "type" : "object",
    "properties" : {
        "sunday" : DAY_REF,
        "monday" : DAY_REF,
        "tuesday" : DAY_REF,
        "wednesday" : DAY_REF,
        "thursday" : DAY_REF,
        "friday" : DAY_REF,
        "saturday" : DAY_REF,
    },
    "required": [
        "sunday",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
    ]
}
```

- __Change Password__
```json
CHANGE_PWD_SCHEMA = {
    "type" : "object",
    "properties" : {
        "password" : {"type" : "string"}
    },
    "required": [
        "password"
    ]
}
```
&#10240;

## &#10240; &#8634; EndPoints &#8635;

- <mark style="background-color: #7bb3ba">&#10240; / &#10240;</mark>&#10240; &#11138; &#10240; [ 'GET' ] &#10240; &#10236; &#10240; Home of ConTime API, <b>endpoint</b> for API documentation.

- <mark style="background-color: #7bb3ba">&#10240; /login &#10240;</mark>
    - GET &#10240; &#11138; &#10240; login using query parameters `email = < email > | password = < password >, type = ( < company > or < employee > )` if login successfully return the respective ID.

- <mark style="background-color: #7bb3ba">&#10240; /employee &#10240;</mark>
    - GET &#10240; &#11138; &#10240; quickly lookup employee's id using query parameter `email = < email >`

- <mark style="background-color: #7bb3ba">&#10240; /companies &#10240;</mark>
    - GET &#10240; &#11138; &#10240; list of all the companies.
    - POST &#10240; &#11138; &#10240; create a new company in accordance with the company's schema above.

- <mark style="background-color: #7bb3ba">&#10240; /companies/< id > &#10240;</mark>
    - GET &#10240; &#11138; &#10240; get company by id.
    - PUT &#10240; &#11138; &#10240; change company's password
    - DELETE &#10240; &#11138; &#10240; delete company permanetly.

- <mark style="background-color: #7bb3ba">&#10240; /companies/< id >/employees &#10240;</mark>
    - GET &#10240; &#11138; &#10240; returns all of company's employees.
    - PUT &#10240; &#11138; &#10240; request employee to work for company using the query parameter <b>`employee_id = < id >`</b>
    - DELETE &#10240; &#11138; &#10240; delete employee from company using the query parameter <b>`employee_id = < id >`</b>.

- <mark style="background-color: #7bb3ba">&#10240; /employees &#10240;</mark>
    - GET &#10240; &#11138; &#10240; list of all the employees.
    - POST &#10240; &#11138; &#10240; create a new employee in accordance with the employee's schema above.

- <mark style="background-color: #7bb3ba">&#10240; /employees/< id > &#10240;</mark>
    - GET &#10240; &#11138; &#10240; get employee by id.
    - PUT &#10240; &#11138; &#10240; change employee's password
    - DELETE &#10240; &#11138; &#10240; delete employee permanetly.

- <mark style="background-color: #7bb3ba">&#10240; /employees/< id >/companies &#10240;</mark>
    - GET &#10240; &#11138; &#10240; returns a list all of the companies employee works for.
    - PUT &#10240; &#11138; &#10240; accept job offer to work for a company using the query parameter <b>`company_id = < id >`</b> and <b>`status = < accept > || < decline >`</b>
    - DELETE &#10240; &#11138; &#10240; leave a company using the query parameter <b>`company_id = < id >`</b>.

- <mark style="background-color: #7bb3ba">&#10240; /calendars &#10240;</mark>
    - GET &#10240; &#11138; &#10240; list of all calendars

- <mark style="background-color: #7bb3ba">&#10240; /calendars/< id > &#10240;</mark>
    - GET &#10240; &#11138; &#10240; get calendar by id.

- <mark style="background-color: #7bb3ba">&#10240; /calendars/employees/< employee_id > &#10240;</mark>
    - GET &#10240; &#11138; &#10240; get all calendars for employee_id

- <mark style="background-color: #7bb3ba">&#10240; /calendars/companies/< company_id > &#10240;</mark>
    - GET &#10240; &#11138; &#10240; get all calendars for company_id

- <mark style="background-color: #7bb3ba">&#10240; calendars/companies/< company_id >/employees/< employee_id > &#10240;</mark>
    - GET &#10240; &#11138; &#10240; return all of employee's calendars for a specific company

- <mark style="background-color: #7bb3ba">&#10240; calendars/companies/< company_id >/employees/< employee_id >/current &#10240;</mark>
    - PUT &#10240; &#11138; &#10240; create current weekly calendar, if current calendar already exists UPDATE in accordance with the calendar's schema above.

Visit API -> ## [api.contime.work](https://api.contime.work/)
&#10240;<br>
<hr>
&#10240;<br>
&#10240; &#10240; &#10240; Author: Marcelo Martins<br>
&#10240; &#10240; &#10240; GitHub: @matxa<br>
&#10240; &#10240; &#10240; Email: matxa21@gmail.com<br>
&#10240;
<hr>
