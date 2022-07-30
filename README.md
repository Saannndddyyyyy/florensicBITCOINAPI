# florensicBITCOINAPI

Crypto Price Alert Web Application's Core Backend, developed as a recruitment task for Krypto
Tech Stack:

BACKEND: PYTHON -FLASK FOR WEB APPLICATION FRAMEWORK
DATABASE: SQLITE
Object Relational Mapper: SQLALCHEMY

API TESTING: POSTMAN
2 MODES:
CONFIG MODE - DEFAULT {CREATE ALERT,DELETE ALERT, FETCH ALERT BY FILTER}
ACTIVATED MODE - EMAIL MODE ENDPOINT
HOMEPAGE : http://127.0.0.1:5000

parameters: u_id - user id, a_id - alert id, a_target - target price



CREATE:
/alerts/create - POST Requests
parameters: u_id - user id, a_id - alert id, a_target - target price

DELETE:

parameters: a_id - alert id

Status is set to created when an alert is made using the POST call
/alerts/delete - PUT Requests

FILTER:
parameters: a_id - alert id
/alerts - GET Requests

WEB APP IS ALSO CONFIGURED FOR DOCKERIZATION
ACCESS TOKEN VALIDITY: 60MINS

