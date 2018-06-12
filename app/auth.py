from flask_restful import Resource, reqparse, fields
from .inputfields import user_inputs
from .model import Users
from .main import unauthorized, save_item
from validate_email import validate_email


class UserRegister(Resource):
    """Register a new user.  URL: /auth/register/   Request method: POST"""

    def post(self):
        """ Add a user """
        parser = reqparse.RequestParser()
        parser.add_argument("fname", required=True,
                            help="Please enter the First Name.")
        parser.add_argument("sname", required=True,
                            help="Please enter the Second Name.")
        parser.add_argument("lname", required=True,
                            help="Please enter the Last Name.")
        parser.add_argument("username", required=True,
                            help="Please enter a username.")
        parser.add_argument("password", required=True,
                            help="Please enter a password.")
        parser.add_argument("email", required=True,
                            help="Please enter an Email.")
        parser.add_argument("category", required=True,
                            help="Use 1 = Teacher, 2 = Student")

        args = parser.parse_args()
        is_valid = validate_email(args["email"])
        if not is_valid:
            return unauthorized("Error: Insert valid email address")
        fname, sname, lname, username, password, email, category = args["fname"], args["sname"], args["lname"], args[
            "username"], args["password"], args["email"], args["category"]
        user = Users(username=username, password=password,
                     email=email, fname=fname, sname=sname, lname=lname, category=category)
        return save_item(name="username",
                         item=user,
                         serializer=user_inputs,
                         is_user=True,
                         is_subject=False
                         )


class Login(Resource):
    """  URL: /auth/login/ Request method: POST"""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True,
                            help="Please enter a username.")
        parser.add_argument("password", required=True,
                            help="Please enter a password.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]

        if username and password:
            user = Users.query.filter_by(username=username).first()
        else:
            return {"message": "Error: Please enter a username and password."}
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {"message": "Successfully logged in. Use the "
                    "token below to make requests.",
                    "token": token.decode("ascii")}
        else:
            return unauthorized("Error: Invalid username and/or password.")
