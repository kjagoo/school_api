
import os
from run import app
from flask import Flask
from app.config import app_config
from flask_testing import TestCase
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
import json
import nose
from app.model import db, Users, UserRights, Subjects, UserSubject


app.config.from_object(app_config["testing"])


class TestBase(TestCase):
    """ Base configurations for the tests """

    def create_app(self):
        """ Returns app """

        return app

    def setUp(self):
        """ Create test database and set up test client """
        self.app = app.test_client()
        engine = create_engine(os.environ['TESTDB'])
        if not database_exists(engine.url):
            create_database(engine.url)
            # db.drop_all()
            db.create_all()
            db.session.commit()
            user1 = Users(username="joshua", password="joshua",
                          email="kagenyi1@gmail.com", fname="joshua", sname="joshua", lname="joshua", category=1)
            user2 = Users(username="joshua2", password="joshua2",
                          email="kagenyi2@gmail.com", fname="joshua2", sname="joshua2", lname="joshua2", category=2)
            user3 = Users(username="joshua3", password="joshua2",
                          email="kagenyi3@gmail.com", fname="joshua2", sname="joshua2", lname="joshua2", category=3)
            subject1 = Subjects(name="Artificial Intelligence",
                                description="Computer Science AI, SC0AI",
                                created_by=1)
            subject2 = Subjects(name="Human Psychology",
                                description="Sociology, S0HP",
                                created_by=1)
            userrights1 = UserRights(name="Admin")
            userrights2 = UserRights(name="Teacher")
            userrights3 = UserRights(name="Student")

            usersubject1 = UserSubject(user=2, subject=1)
            usersubject2 = UserSubject(user=3, subject=1)
            usersubject3 = UserSubject(user=3, subject=2)

            db.session.add(user1)
            db.session.add(user2)
            db.session.add(user3)
            db.session.add(subject1)
            db.session.add(subject2)
            db.session.add(userrights1)
            db.session.add(userrights2)
            db.session.add(userrights3)
            db.session.add(usersubject1)
            db.session.add(usersubject2)
            db.session.add(usersubject3)

            db.session.commit()
           

    def test_index(self):
        """ Test response to the index route """
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "Welcome to the School API."
                                  " You can get started by :"
                                  "1. Login "
                                  "2. Register a new user "})

    def tearDown(self):
        """ Destroy test database """
        # engine = drop_database(os.environ['TESTDB'])
        # drop_database(engine.url)


if __name__ == "__main__":
    nose.run()
