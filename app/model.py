from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from . import db, app

# migrate = Migrate(app, db)
# manager = Manager(app)

# manager.add_command('db', MigrateCommand)


class Users(db.Model):
    """   Users   """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True)
    fname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    category = db.Column(db.Integer)

    @property
    def password(self):
        """Prevents access to password property"""
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """Sets password to a hashed password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Checks if password matches"""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=20000):
        """Generating an authentication token that expires in 20 minutes"""
        serializer = Serializer(app.config["SECRET_KEY"],
                                expires_in=expiration)
        return serializer.dumps({"email": self.email,
                                 "username": self.username})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            """When token is valid but expired """
            return None
        except BadSignature:
            """When token is invalid """
            return None

        user = Users.query.filter_by(email=data["email"]).first()
        return user

    def __repr__(self):
        return "<User: %r>" % self.username


class UserSubject(db.Model):
    """ create User- Subject table """

    __tablename__ = "usersubject"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("users.id"))
    subject = db.Column(db.Integer, db.ForeignKey("subject.id"))
    is_main = db.Column(db.Boolean)
    users = db.relationship(
        "Users", backref=db.backref("users", lazy="dynamic"))
    

    subjects = db.relationship("Subjects",
                            backref=db.backref("subject"), lazy="select")
    users_subjects = db.UniqueConstraint('users', 'subjects')


    def __repr__(self):
        return "<UserSubjects: %r>" % self.subject


class UserRights(db.Model):
    """ Creates Access rights  """

    __tablename__ = "userright"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String)
    
    def __repr__(self):
        return "<UserRights: %r>" % self.name


class Subjects(db.Model):
    """ Creates subjects """

    __tablename__ = "subject"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer)

    def __repr__(self):
        return "<Subjects: %r>" % self.name


if __name__ == '__main__':
    manager.run()
