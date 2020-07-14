import pytest
import datetime
from django.utils import timezone
from unittest.mock import patch, Mock
from django.contrib.auth.models import User
from rested.validation import *
from rested.test import TestCase

a = {}
b = {"a": 1}
c = {"a": 1, "b": {"c": 2, "d": {"e": 3}}}
d = {"b": {"d": {"e": 3}}}
e = {"a": 1, "b": {"c": 2, "d": 3}}

class ValidateTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='user', email='user@test.com', password='user')
        User.objects.create_user(username='admin', email='admin@test.com', password='admin', is_superuser=True)
        User.objects.create_user(username='staff', email='staff@test.com', password='staff', is_staff=True)
        User.objects.create_user(username='inactive', email='inactive@test.com', password='inactive', is_active=False)

    def test_validator(self):
        assert v.to.string.execute("1") == "1"
        assert v.to.integer.execute("1") == 1
        assert v.to.string.execute(1) == "1"
        assert v.to.integer.execute(1) == 1

        assert v.am.integer.execute(1) == 1
        assert v.am.string.execute("1") == "1"
        with pytest.raises(ValidationError): v.am.integer.execute("1")
        with pytest.raises(ValidationError): v.am.string.execute(1)
        assert v.to.string.am.string.to.integer.am.integer.execute(1) == 1

        assert len(v.am.chain) == 1
        assert len(v.to.chain) == 1
        assert len(v.accepts.chain) == 1
        assert len(v.optional.chain) == 1

    def test_dig(self):
        with pytest.raises(KeyError): dig(None, 'a')
        with pytest.raises(KeyError): dig(1, 'a')
        with pytest.raises(KeyError): dig({'1': 1}, 'a')
        with pytest.raises(KeyError): dig({'1': {'3': 'b'}}, ['1', '2'])
        with pytest.raises(KeyError): dig({'1': {'2': 'b'}}, ['1', '2', '3'])
        assert dig({'1': None}, '1') is None
        assert dig({'1': 1}, '1') == 1
        assert dig({'1': 1}, ['1']) == 1
        assert dig({'1': 'a'}, '1') == 'a'
        assert dig({'1': {'2': 'b'}}, ['1', '2']) == 'b'

    def test_accepts(self):
        errors, valid = check({}, {"a": v.accepts})
        assert errors == {"a": 'expected_defined'} and valid == {}

        errors, valid = check({'a': None}, {"a": v.accepts.null})
        assert errors == {} and valid == {'a': None}

        errors, valid = check({'a': None}, {"a": v.accepts.null.am.integer})
        assert errors == {} and valid == {'a': None}

        errors, valid = check({'a': None}, {"a": v.accepts.am.integer})
        assert errors == {"a": 'expected_integer'} and valid == {}

        errors, valid = check({'a': 'hi'}, {'a': v.accepts.any(['hi']).integer})
        assert errors == {} and valid == {'a': 'hi'}

        errors, valid = check({'a': 'bye'}, {'a': v.accepts.any(['hi']).integer})
        assert errors == {"a": 'expected_integer'} and valid == {}

        errors, valid = check({'a': 'bye'}, {'a': v.accepts.any(['hi', 'bye']).integer})
        assert errors == {} and valid == {'a': 'bye'}

    def test_validate(self):
        errors, valid = check({}, {"a": v.am})
        assert errors == {"a": 'expected_defined'} and valid == {}

        errors, valid = check({"a": "b"}, {"a": v.am})
        assert errors == {} and valid == {"a": "b"}

        errors, valid = check({"a": "b"}, {"a": v.am.integer})
        assert errors == {"a": 'expected_integer'} and valid == {}

    def test_convert(self):
        errors, valid = check({}, {"a": v.to})
        assert errors == {"a": 'expected_defined'} and valid == {}

        errors, valid = check({"a": 1}, {"a": v.to})
        assert errors == {} and valid == {"a": 1}

        errors, valid = check({"a": 1}, {"a": v.to.string.am.string})
        assert errors == {} and valid == {"a": "1"}

        errors, valid = check({"a": 1}, {"a": v.to.string.am.string.to.integer.am.integer})
        assert errors == {} and valid == {"a": 1}

    def test_optional(self):
        errors, valid = check({}, {"a": v.optional})
        assert errors == {} and valid == {}

        errors, valid = check({"a": "b"}, {"a": v.optional.string})
        assert errors == {} and valid == {"a": "b"}

        errors, valid = check({"a": 1}, {"a": v.optional.string})
        assert errors == {"a": "expected_string"} and valid == {}

    def test_check(self):
        errors, valid = check({}, {})
        assert errors == {} and valid == {}

        errors, valid = check(c, {"a": v.am, "b": {"c": v.am, "d": {"e": v.am}}})
        assert errors == {} and valid == c

        errors, valid = check(c, {"a": v.am, "b": {"c": v.am, "d": {"e": v.am, "f": v.am}}})
        assert errors == {"b": {"d": {"f": "expected_defined"}}} and valid == c

    def test_validate_data(self):
        response = self.post("/vecho", c)
        assert response.status_code == 200
        assert response.data == c

        response = self.post("/vecho", b)
        assert response.status_code == 400
        assert response.data == {'b': {'c': 'expected_defined', 'd': 'expected_defined'}}

    def test_validate_query(self):
        response = self.get("/vquery", {'age': 12})
        assert response.status_code == 200
        assert response.data == {'age': 12}
        #
        # response = self.get("/vparams/12", b)
        # assert response.status_code == 400
        # assert response.data == {'b': {'c': 'expected_defined', 'd': 'expected_defined'}}

    # we could have validate package up args and kwargs, then unpackage them and pass to view
    # after validation, I think its the right way to go just maybe not that useful of a feature
    # and it is a bit strange to have a url 400 based on the url so theres that too
    # def test_validate_url_params(self):
    #     response = self.get("/vpurl", c)
    #     assert response.status_code == 404
    #
    #     response = self.get("/vpurl/12", c)
    #     assert response.status_code == 200
    #     assert response.data == {'num': '12'}
