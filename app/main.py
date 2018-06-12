from flask import g, jsonify, request
from flask_restful import Resource, marshal
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from .model import Users, Subjects, UserSubject, UserRights
from . import db, app


auth = HTTPBasicAuth()


@auth.error_handler
def unauthorized(message=None):
    """Returns an error message."""
    if not message:
        message = "Error: Restricted unauthorised access."
    return jsonify({"message": message}), 403


def authorized_user_subjects(function):
    def auth_wrapper(*args, **kwargs):
        g.subject = User_Subject.query.filter_by(id=kwargs["id"]).first()
        try:
            if g.subject.created_by == g.user.id:
                return function(*args, **kwargs)
            elif g.user.id == 0:
                return function(*args, **kwargs)
            return unauthorized()
        except:
            return unauthorized("Error: The Subject doesn't exist.")
    return auth_wrapper


# def authorized_user_item(function):
#     def auth_wrapper(*args, **kwargs):
#         g.item = Users.query.filter_by(id=kwargs["id"],
#                                                  id=kwargs["item_id"]).first()
#         try:
#             if g.item.created_by == g.user.id:
#                 return function(*args, **kwargs)
#             return unauthorized()
#         except:
#             return unauthorized("Error: The student doesn't exist.")
#     return auth_wrapper


@app.before_request
def before_request():
    """  Validates token.
    Ran before requests apart from user registration, login and index.
    """
    if request.endpoint and request.endpoint not in ["login", "userregister",
                                                     "index"]:
        token = request.headers.get("token")
        if token is not None:
            user = Users.verify_auth_token(token)
            if user:
                g.user = user
            else:
                return unauthorized("Error: Invalid token."), 401
        else:
            return unauthorized("Error: Authentication token not found!"), 401


def save_item(**kwargs):
    """
    Add a user or subject to the database.
    Also handles integrity errors.
    Arguments:
        kwargs["name"]: The title of the item to be added to the database.
        kwargs["item"]: The item to be added to the database.
        kwargs["serializer"]: The marshal serializer.
        kwargs["is_user"]: The flag used to identify users.
        kwargs["is_subject"]: The flag used to identify subjects.
        kwargs["is_userright"]: The flag used to identify userrights .
    """
    try:
        db.session.add(kwargs["item"])
        db.session.commit()
        if kwargs["is_user"]:
            item_type = "user"
        elif kwargs["is_subject"]:
            item_type = "subject"
        elif kwargs["is_userright"]:
            item_type = "user right"
        # include token on registration
        if kwargs["is_user"]:
            user = Users.query.filter_by(
                username=kwargs["item"].username).first()
            token = user.generate_auth_token()
            message = {"message": "Successfully added " +
                       item_type + ".", "token": token.decode("ascii")}
        else:
            message = {"message": "Successfully added " +
                       item_type + "."}

        response = marshal(kwargs["item"], kwargs["serializer"])
        response.update(message)
        return response, 201

    except IntegrityError:
        """When adding an item that already exists"""
        db.session.rollback()
        return {"error": "The " + kwargs["name"] + " already exists."}


def delete_item(item, name, **kwargs):
    """
    Delete a bucket list or bucket list item from the database.
    Arguments:
        item = The item to be deleted.
        name = The name of the item to be deleted.
        kwargs["is_user"]: The flag used to identify users.
        kwargs["is_subject"]: The flag used to identify subjects.
        kwargs["is_userright"]: The flag used to identify userrights .
    """
    if item:
        db.session.delete(item)
        db.session.commit()
        if kwargs["is_user"]:
            item_type = "user"
        elif kwargs["is_subject"]:
            item_type = "subject"
        elif kwargs["is_userright"]:
            item_type = "user right"
        return {"message": "Successfully deleted " + item_type + ": '" +
                name + "'."}
    else:
        return {"message": "Delete was unsuccessful. Please try again!"}


def edit_item(**kwargs):
    """
    Edit a bucket list or bucket list item.
    Arguments:
        kwargs["name"]: The title of the item to be edited.
        kwargs["item"]: The item to be edited.
        kwargs["serializer"]: The marshal serializer.
        kwargs["is_user"]: The flag used to identify users.
        kwargs["is_subject"]: The flag used to identify subjects.
        kwargs["is_userright"]: The flag used to identify userrights ..
    """
    db.session.add(kwargs["item"])
    db.session.commit()
    if kwargs["is_user"]:
            item_type = "user"
    elif kwargs["is_subject"]:
        item_type = "subject"
    elif kwargs["is_userright"]:
        item_type = "user right"
    message = {"message": "Successfully updated " + item_type + "."}
    response = marshal(kwargs["item"], kwargs["serializer"])
    response.update(message)
    return response


class Index(Resource):
    """ Manage responses to the index route.
    URL: /  Request method: GET
    """

    def get(self):
        """ Return a welcome message """
        return {"message": "Welcome to the School API."
                " You can get started by :"
                "1. Login "
                "2. Register a new user "}


class Subject(Resource):
    """ Manage responses to the index route.
    URL: /  Request method: GET
    """
    def get(self):
        """ Return a welcome message """
        return {}

    def post(self):
        return {}


