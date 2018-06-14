from app import api, app
from app.main import Index, Subject, SubjectsId, MySubject
from app.auth import UserRegister, Login

""" Defining the API endpoints """
api.add_resource(Index, "/")
api.add_resource(UserRegister, "/auth/register/")
api.add_resource(Login, "/auth/login/")
api.add_resource(Subject, "/subjects/")
api.add_resource(SubjectsId, "/subjects/<id>")
api.add_resource(MySubject, "/mysubjects/")

if __name__ == "__main__":
    app.run()
