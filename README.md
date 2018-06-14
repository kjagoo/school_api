# School Api
This is a Flask web service application which manages students, teacher and subjects. 
It implements token based authentication to manage security.
It allows 
- admins to add new subjects , teachers and students
- delete subjects , teachers and students
- Teacher to view students doing his/her subject
- Students having only one major subject, and do other subjects 


# Requirements
- Postgres Database
- Python Flask api

**[# Installation](url)**

1. Clone the repo on github
   - `https://github.com/kjagoo/school_api`
   
2. Install requirements
   - `pip install -r requirements.txt`
   
3. Create database school 
   - edit in `manage.py` `postgresql+psycopg2://[username]:[password]@localhost:5432/school`
   - `createdb school`
   - `python manage.py db init`
   - `python manage.py db migrate`


**[#Running the Program](url)**

`python run.py`

**[#Usage Routes](url)**

register new user
- `POST` - `127.0.0.1:5000/auth/register/`

login
- `POST` - `127.0.0.1:5000/auth/login/`

get list of all subjects
- `GET` - `127.0.0.1:5000/subjects/`

add a subject
- `POST` - `127.0.0.1:5000/subject/`

edit a subject
- `PUT` - `127.0.0.1:5000/subject/<id>`

delete a subject
- `DELETE` - `127.0.0.1:5000/subject/<id>`

get and display a specific subject
- `GET` - `127.0.0.1:5000/subject/<id>`



**[#Tests](url)**

Setup test environment by :
   - edit in `envvariables.py` `postgresql+psycopg2://[username]:[password]@localhost:5432/testbucketlist`
   - `nosetests --with-coverage --cover-erase --cover-package=tests`
   


**[# Credits](url)**

Joshua Kagenyi 