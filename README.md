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

    <b>/employer/<i>id</i>/employee/<i>employee_id</i></b>:
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
</pre>
