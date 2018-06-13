import json
from . import TestBase
from datetime import datetime


class TestSchool(TestBase):
    """ Test operations on school api """

    def get_token(self):
        """ Returns authentication token """
        self.user = {"username": "joshua", "password": "joshua"}
        response = self.app.post("/auth/login/", data=self.user)
        output = json.loads(response.data.decode('utf-8'))
        token = output.get("token").encode("ascii")
        self.token = token
        return {"token": token}

    def test_no_token(self):
        """ Test that users must provide a token to make responses """
        self.subject = {"name": "english",
                        "description":
                        "Language semantics"}
        response = self.app.post("/subjects/", data=self.subject)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode('utf-8'))
        self.assertIn("Error: Authentication token not found!",
                      output["message"])

    def test_invalid_token(self):
        """ Test that invalid tokens cannot be used """
        self.subject = {"name": "Mathematics",
                           "description":
                           "Introduction to calculus"}
        invalid_token = {"token": 12345}
        response = self.app.post("/subjects/", data=self.subject,
                                 headers=invalid_token)
        self.assertEqual(response.status_code, 401)
        output = json.loads(response.data.decode('utf-8'))
        self.assertIn("Error: Invalid token", output["message"])

    def test_add_subject(self):
        """ Test addition of subjects """
        self.subject = {"name": "Math Calculus 1" +
                           str(datetime.now()),
                           "description":
                           "Introduction to Calculus"}
        response = self.app.post(
            "/subjects/", data=self.subject, headers=self.get_token())
        self.assertEqual(response.status_code, 201)
        output = json.loads(response.data.decode('utf-8'))
        print (response.data)
        self.assertTrue("Successfully added subject" in output["message"])
        self.assertIn(self.subject["name"], response.data.decode('utf-8'))
        self.assertIn(self.subject["description"],
                      response.data.decode('utf-8'))

    def test_add_subjects_no_duplicates(self):
        """ Test addition of dublicate subjects is not allowed """
        self.subject = {"name": "Artificial Intelligence",
                           "description":
                           "Computer Science AI, SC0AI"}
        response = self.app.post(
            "/subjects/", data=self.subject, headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        print (response.data)
        self.assertTrue("The name already exists" in output["error"])

    def test_delete_subject(self):
        """ Test delete subjects """
        response = self.app.delete("/subjects/3", headers=self.get_token())
        output = json.loads(response.data.decode('utf-8'))
        print output
        if response.status_code == 403:
            self.assertIn("Error: The subject doesn't exist.",
                          output["message"])
        else:
            self.assertEqual(response.status_code, 200)

            self.assertIn("Successfully deleted subject",
                          output["message"])

    def test_edit_subject(self):
        """ Test updating of subjects"""
        self.subject = {"name": "Home science class",
                        "description": "How to cook sushi"}
        response = self.app.put("/subjects/3",
                                data=self.subject,
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        self.assertIn("Successfully updated subject list.", output["message"])
        self.assertIn(self.subject["name"], response.data.decode('utf-8'))
        self.assertIn(self.subject["description"],
                      response.data.decode('utf-8'))

    def test_get_subject_id(self):
        """ Test that specified ID subject is displayed """
        # Get subject whose ID is 2
        response = self.app.get("/subjects/2",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        subject1 = json.loads(response.data.decode('utf-8'))
        self.assertEqual(subject1.get("name"), "Human Psychology")

    def test_get_invalid_subject_id(self):
        """ Test error raised on invalid subject ID """
        response = self.app.get("/subjects/2000",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 403)
        output = json.loads(response.data.decode('utf-8'))
        self.assertIn("Error: The subject doesn't exist.",
                      output["message"])


    def test_get_subjects(self):
        """ Test that all subjects  are displayed """
        response = self.app.get("/subjects/",
                                headers=self.get_token())
        self.assertEqual(response.status_code, 200)
        output = json.loads(response.data.decode('utf-8'))
        output = output["subjects"]

        # subjects are displayed
        self.assertTrue(any(d['name'] == 'Human Psychology' for d in output))
