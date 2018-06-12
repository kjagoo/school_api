from app import api, app
from app.main import Index
from app.auth import UserRegister, Login

""" Defining the API endpoints """
api.add_resource(Index, "/")
api.add_resource(UserRegister, "/auth/register/")
api.add_resource(Login, "/auth/login/")

if __name__ == "__main__":
    app.run()
