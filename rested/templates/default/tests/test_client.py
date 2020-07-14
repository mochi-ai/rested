import pytest
import unittest
from rested.test.fixtures import database
from django.test import Client
from api.models import Question


db = database(reset_sequences=False, autouse=True)

#@pytest.mark.django_db
class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        response = self.client.get('/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 302)

    def test_sequence(self):
        q = Question.create().save()
        assert q.id == 1

    def test_sequence_again(self):
        q = Question.create().save()
        assert q.id == 1
