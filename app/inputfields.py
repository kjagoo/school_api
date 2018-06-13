from flask_restful import fields


user_inputs = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "fname": fields.String,
    "sname": fields.String,
    "lname": fields.String,
    "category": fields.Integer
}

subject_inputs = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "date_created": fields.DateTime(dt_format='rfc822'),
    "date_modified": fields.DateTime(dt_format='rfc822'),
    "created_by": fields.String,
   
}
