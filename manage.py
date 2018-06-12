import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DEVELOPMENTDB']

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class UserSubject(db.Model):
    """ create User- Subject table """

    __tablename__ = "usersubject"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("users.id"))
    subject = db.Column(db.Integer, db.ForeignKey("subjects.id"))

    def __repr__(self):
        return "<UserSubjects: %r>" % self.subject.name


class UserRights(db.Model):
    """ Creates Access rights  """

    __tablename__ = "userright"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    
    def __repr__(self):
        return "<UserRights: %r>" % self.name


class Subjects(db.Model):
    """ Creates subjects """

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2), unique=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.utcnow)

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    
    def __repr__(self):
        return "<Subjects: %r>" % self.title


class Users(db.Model):
    """   Users   """
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(128))
    fname = db.Column(db.String(100))
    sname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    category = db.relationship("UserRights", backref=db.backref("user_right", lazy="dynamic")) 
    
if __name__ == '__main__':
    manager.run()
