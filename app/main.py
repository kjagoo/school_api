from flask import g, jsonify, request
import json
from flask_restful import Resource, marshal
from flask_restful import reqparse
from flask_httpauth import HTTPBasicAuth
from sqlalchemy.exc import IntegrityError
from .inputfields import subject_inputs, usersubject_inputs
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
        g.subject = Subjects.query.filter_by(id=kwargs["id"]).first()
        print g.subject
        try:
            if g.subject.id:
                return function(*args, **kwargs)
            return unauthorized()
        except:
            return unauthorized("Error: The subject doesn't exist.")
    return auth_wrapper


def authorized_user_mysubjects(function):
    def auth_wrapper(*args, **kwargs):
        g.subjects = Subjects.query.join(UserSubject).filter_by(user=g.user.id).all()
        print g.subjects
        return function(*args, **kwargs)
        # try:
        #     if g.subjects:
        #         return function(*args, **kwargs)
        #     return unauthorized()
        # except Exception as e:
        #     return unauthorized("Error: The subject doesn't exist.2")
    return auth_wrapper


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
        elif kwargs["is_usersubject"]:
            item_type = "user subject"
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
    Delete a user or subject  from the database.
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
        elif kwargs["is_usersubject"]:
            item_type = "user subject"
        return {"message": "Successfully deleted " + item_type + ": '" +
                name + "'."}
    else:
        return {"message": "Delete was unsuccessful. Please try again!"}


def edit_item(**kwargs):
    """
    Edit a user or subject.
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
    elif kwargs["is_usersubject"]:
            item_type = "user subject"
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
    """ URL: /subjects/  Request methods: GET, POST """

    def get(self):
        """ Get all subjects 
        """
        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        search = args.get("q")

        if search:
            kwargs.update({"name": search})
            error_message = {"message": "The subject '" + search +
                                "' does not exist."}

        subjects = Subjects.query.paginate(page=page,
                                                        per_page=limit,
                                                        error_out=False)
        total_pages = subjects.pages
        has_next_page = subjects.has_next
        has_previous_page = subjects.has_prev

        next_page = "None"
        previous_page = "None"
        if has_next_page:
            next_page = str(request.url_root) + "/subjects?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)

        if has_previous_page:
            previous_page = request.url_root + "/subjects?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)

        subjects = subjects.items

        output = {"subjects": marshal(subjects, subject_inputs),
                    "has_next_page": has_next_page,
                    "total_pages": total_pages,
                    "previous_page": previous_page,
                    "next_page": next_page
                    }
        error_message = {"subjects":
                         [{"message":
                           "Subject Lists are Empty"}],
                         "has_next_page": has_next_page,
                         "total_pages": total_pages,
                         "previous_page": previous_page,
                         "next_page": next_page}

        if subjects:
            return output
        else:
            return error_message


    def post(self):
        """ Add a Subject list """
        parser = reqparse.RequestParser()
        parser.add_argument("name", required=True, help="No title provided.")
        parser.add_argument("description", type=str, default="")
        args = parser.parse_args()
        name, description = args["name"], args["description"]
        subject = Subjects(name=name,
                          description=description,
                          created_by=g.user.id)

        return save_item(name="name",
                         item=subject,
                         serializer=subject_inputs,
                         is_user=False,
                         is_subject=True,
                         is_userright=False)


class SubjectsId(Resource):
    """ URL: /subjects/<id>   Request methods: GET, PUT, DELETE   """
    @authorized_user_subjects
    def get(self, id):
        """ Get a subject list """
        return marshal(g.subject, subject_inputs)

    @authorized_user_subjects
    def put(self, id):
        """ Edit a subject """
        parser = reqparse.RequestParser()
        parser.add_argument("name",
                            required=True,
                            help="No title provided.")
        parser.add_argument("description", type=str, default="")
        args = parser.parse_args()
        name, description = args["name"], args["description"]
        g.subject.name = name
        g.subject.description = description
        return edit_item(name="name",
                         item=g.subject,
                         serializer=subject_inputs,
                         is_user=False,
                         is_subject=True,
                         is_userright=False)


    @authorized_user_subjects
    def delete(self, id):
        """ Delete a subject """
        return delete_item(g.subject,
                           g.subject.name,
                           is_user=False,
                           is_subject=True,
                           is_userright=False)


class MySubject(Resource):
    """ URL: /mysubjects/  Request methods: GET, POST """

    @authorized_user_mysubjects
    def get(self):
        """ Get all mysubjects 
        """
        # args = request.args.to_dict()
        # page = int(args.get("page", 1))
        # limit = int(args.get("limit", 20))
        # search = args.get("q")

        # if search:
        #     kwargs.update({"id": search})
        #     error_message = {"message": "The subject '" + search +
        #                      "' does not exist."}

        # subjects = UserSubject.query.paginate(page=page,per_page=limit,error_out=False)
        
        # total_pages = subjects.pages
        # has_next_page = subjects.has_next
        # has_previous_page = subjects.has_prev

        # next_page = "None"
        # previous_page = "None"
        # if has_next_page:
        #     next_page = str(request.url_root) + "/mysubjects?" + \
        #         "limit=" + str(limit) + "&page=" + str(page + 1)

        # if has_previous_page:
        #     previous_page = request.url_root + "/mysubjects?" + \
        #         "limit=" + str(limit) + "&page=" + str(page - 1)

        # subjects = subjects.items

        # output = {"subjects": marshal(subjects, subject_inputs),
        #           "has_next_page": has_next_page,
        #           "total_pages": total_pages,
        #           "previous_page": previous_page,
        #           "next_page": next_page
        #           }
        # error_message = {"subjects":
        #                  [{"message":
        #                    "Subject Lists are Empty"}],
        #                  "has_next_page": has_next_page,
        #                  "total_pages": total_pages,
        #                  "previous_page": previous_page,
        #  
        #                "next_page": next_page}
        
        subjects =  Subjects.query.join(UserSubject).filter_by(user=g.user.id).all()
        subjects = {'name': dict(subjects)}
        if subjects:
            return g.subjects
        else:
            return error_message


    def post(self):
        """ Add a Subject list """
        parser = reqparse.RequestParser()
        parser.add_argument("subject", required=True,
                            help="No title provided.")
        parser.add_argument("is_main", required=True,
                            help="Select if your major or main teaching subject.")
        args = parser.parse_args()
        if args["is_main"] == 'true':
            args["is_main"] = True
        else:
            args["is_main"] = False
        name, is_main = args["subject"],args["is_main"]
        is_main
        subject = UserSubject(subject=name, is_main=is_main,
                              user=g.user.id)

        return save_item(name="name",
                         item=subject,
                         serializer=usersubject_inputs,
                         is_user=False,
                         is_subject=False,
                         is_userright=False,
                         is_usersubject=True
                         )
