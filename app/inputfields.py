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
