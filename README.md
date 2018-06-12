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
- `DELETE` - `127.0.0.1:5000/bucketlists/<id>`

get and display a specific subject
- `GET` - `127.0.0.1:5000/bucketlists/<id>`

add bucketlist item
- `POST` - `127.0.0.1:5000/bucketlists/<id>/items/`

get a specific bucketlist item
- `GET` - `127.0.0.1:5000/bucketlists/<id>/items/<id>`

edit and update a bucketlist item
- `PUT` - `127.0.0.1:5000/bucketlists/<id>/items/<id>`

delete bucketlist item
- `DELETE` - `127.0.0.1:5000/bucketlists/<id>/items/<id>`

**[#Tests](url)**

Setup test environment by :
   - edit in `testmanage.py` `postgresql+psycopg2://[username]:[password]@localhost:5432/testbucketlist`
   - `createdb testbucketlist`
   - `python testmanage.py db init`
   - `python testmanage.py db migrate`
   - `python testmanage.py db upgrade`
   - `python testmanage.py seed`
   
<img width="723" alt="screen shot 2017-01-27 at 7 57 29 am" src="https://cloud.githubusercontent.com/assets/8224798/22361045/e6c6a506-e466-11e6-914c-60fb57207741.png">


**[#Usage guide](url)**
- register a new user
 `POST` - `127.0.0.1:5000/auth/register/`
<img width="1047" alt="screen shot 2017-01-25 at 3 28 42 pm" src="https://cloud.githubusercontent.com/assets/8224798/22339329/a3c303b0-e3fa-11e6-9541-045cb35ab77c.png">

- login using credentials after registration
 `POST` - `127.0.0.1:5000/auth/login/`
<img width="1045" alt="screen shot 2017-01-25 at 3 29 41 pm" src="https://cloud.githubusercontent.com/assets/8224798/22339301/8779cc3e-e3fa-11e6-96f8-a32406bd3890.png">

- get bucketlist and use the token provided passed as header
 `GET` - `127.0.0.1:5000/bucketlists/`
<img width="1132" alt="screen shot 2017-01-25 at 3 26 44 pm" src="https://cloud.githubusercontent.com/assets/8224798/22339337/ad1f00b2-e3fa-11e6-978d-d20c46402655.png">

- add bucketlist
 `POST` - `127.0.0.1:5000/bucketlists/`
<img width="926" alt="screen shot 2017-01-27 at 7 37 52 am" src="https://cloud.githubusercontent.com/assets/8224798/22360726/974e234e-e463-11e6-8247-86d74b79b6ff.png">

- get bucketlist
 `GET` - `127.0.0.1:5000/bucketlists/`
<img width="1038" alt="screen shot 2017-01-25 at 3 51 34 pm" src="https://cloud.githubusercontent.com/assets/8224798/22339254/64fec90c-e3fa-11e6-82e6-9ca9430b14e0.png">

- add bucketlist item
 `POST` - `127.0.0.1:5000/bucketlists/`
<img width="966" alt="screen shot 2017-01-27 at 7 47 30 am" src="https://cloud.githubusercontent.com/assets/8224798/22360850/efd44f24-e464-11e6-90b6-590b71fea811.png">

**[# Credits](url)**

Joshua Kagenyi 