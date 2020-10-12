# ConTime
Making it easier for (sub)contractors to manage employees' work history.

## API
ConTime's API makes it possible for the backend and frontend technologies to communicate to each other.

### API documentation can be found at /api
<pre>
    - GET -> /api
</pre>

<b>Employer Blueprint API</b>
<pre>
    <b>/api/employer</b>:
        - GET  -> List of all employers in the database
        - POST -> Creates a new employer user - from json body
                  -> required: ["first_name", "last_name", "email"]

    <b>/api/employer/<i>id</i></b>:
        - GET  -> Get employer by id

    <b>/api/employer/<i>id</i>/employee</b>
        - GET  -> Get all employees given employer id

    <b>/api/employer/<i>id</i>/employee/<i>employee_id</i></b>:
        - GET    -> Get employee by id giver employer id
        - DELETE -> Delete employee by id given employer id
</pre>

<b>Employee Blueprint API</b>
<pre>
    <b>/api/employee</b>:
        - GET  -> List of all employees in the database
        - POST -> Creates a new employee user - from json body
                  -> required: ["first_name", "last_name", "email", "employer_id"]

    <b>/api/employee/<i>id</i></b>:
        - GET  -> Get employee by id

    <b>/api/employee/<i>id</i>/employer</b>:
        - GET  -> Get employer of given employee
</pre>

## Modules - Classes

### class BaseUser()
<b>BaseUser is the class in which <i>Employer</i> and <i>Employee</i> classes inherit from</b>
<pre>
<b>__init__()</b>
    - first_name
    - last_name
    - email
    - date_created

<b>object()</b>
    - return a dictionary representing [Employer, Employee] classes.

<b>__str__()</b>
    - return json representation of object() method
</pre>


### class WeekCalendar()
<b>WeekCalendar is a class that generates a weekly calender for employee, given a SUNDAY - week start day</b>
<pre>
<b>__init__()</b>
    - employee_id
    - employer_id
    - is_week_over
    - start_date
    - week_info = start_end_week(self.start_date)
    - end_date
    - week
    - week_id
    - SUN = WorkDescription()
    - MON = WorkDescription()
    - TUE = WorkDescription()
    - WED = WorkDescription()
    - THU = WorkDescription()
    - FRI = WorkDescription()
    - SAT = WorkDescription()

<b>template()</b>
    - return a dictionary with the week days along with job description for each given day using the helper class WorkDescription

<b>get_work_description()</b>
    - acts as a getter function
    - gets all the job description for given day (date)
        -> instance.get_work_description("SUN")
            : returns the job description of day - sunday

<b>set_work_description(day, hour, location, description)</b>
    - acts as a setter function
    - updates the given job descriptions for given day (date)
        -> instance.set_work_description("SUN", 8, "New York", "painted room 21 on 2nd-fl")

<b>calender_id()</b>
    - generates a unique calender id
        -> this is crutial because its makes it possible for one employee to work for multiple employees

<b>object()</b>
    - return a dictionary representation of the WeekCalendar class

<b>__str__()</b>
    - return a json representation of the WeekCalendar class

<b>WorkDescription() class</b>
    - helper class for assinging work descrition
</pre>
