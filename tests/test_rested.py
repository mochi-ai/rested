import datetime
from django.utils import timezone
from unittest.mock import patch, Mock
from pdb import set_trace as debugger
from rested.test import TestCase, Client
from example.models import Person, User


class PathTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='user', email='user@test.com', password='user')
        User.objects.create_user(username='admin', email='admin@test.com', password='admin', is_superuser=True)
        User.objects.create_user(username='staff', email='staff@test.com', password='staff', is_staff=True)
        User.objects.create_user(username='inactive', email='inactive@test.com', password='inactive', is_active=False)

    def test_index(self):
        response = self.client.get("/index")
        assert response.status_code == 200

    def test_params(self):
        data = {"a": "b"}
        assert self.get("/params", params=data).data == data
        assert self.put("/params", params=data).data == data
        assert self.post("/params", params=data).data == data
        assert self.delete("/params", params=data).data == data

    def test_data_json(self):
        data = {"a": "b"}
        assert self.put("/data", data=data).data == data
        assert self.post("/data", data=data).data == data

    def test_data_form(self):
        data = {"a": "b"}
        assert self.client.post("/data", data).json() == data

    def test_get(self):
        assert self.get("/okay").data["payload"] == "get"

    def test_put(self):
        assert self.put("/okay").data["payload"] == "put"

    def test_post(self):
        assert self.post("/okay").data["payload"] == "post"

    def test_delete(self):
        assert self.delete("/okay").data["payload"] == "delete"

    def test_model(self):
        billy = Person.objects.create(name="billy", avatar='blah').save()
        response = self.get(f"/people/{billy.id}")
        assert response.status == 200
        assert response.data['name'] == 'billy'
        assert response.data['avatar'] == 'blah'

    def test_model_set(self):
        jack = Person.objects.create(name="jack").save()
        jill = Person.objects.create(name="jill").save()
        response = self.get("/people")
        assert response.status == 200
        assert str(jack.id) in response.data and response.data[str(jack.id)]['name'] == 'jack' # no int keys in json
        assert str(jill.id) in response.data and response.data[str(jill.id)]['name'] == 'jill'
        assert response.data[str(jack.id)]['avatar'] == ''

    def test_dupes(self):
        assert self.get("/dupe").data["payload"] == 1

    def test_regex(self):
        assert self.get("/a").data["payload"] == "get"
        assert self.get("/ab").data["payload"] == "get"

    def test_decorator(self):
        assert self.get("/decorated").data["payload"] == 7
        assert self.get("/decoratedx2").data["payload"] == 8

    def test_abort(self):
        response = self.get("/boom")
        assert response.data["payload"] == "boom"

    def test_abort_default(self):
        response = self.get("/data")
        assert response.data == {}

    def test_exception(self):
        with self.assertRaises(Exception):
            response = self.client.get("/kaboom")

    def test_tuple_status(self):
        assert self.get("/status").status_code == 444

    def test_auth_public(self):
        response = self.get("/auth/public")
        assert response.status_code == 200

    def test_auth_authenticated(self):
        response = self.get("/auth/authenticated")
        assert response.status_code == 401

        self.client.login(username='user', password='user')
        response = self.get("/auth/authenticated")
        assert response.status_code == 200

    def test_auth_admin(self):
        response = self.get("/auth/admin")
        assert response.status_code == 401

        self.client.login(username='user', password='user')
        response = self.get("/auth/admin")
        assert response.status_code == 403

        self.client.login(username='admin', password='admin')
        response = self.get("/auth/admin")
        assert response.status_code == 200

    def test_auth_staff(self):
        response = self.get("/auth/staff")
        assert response.status_code == 401

        self.client.login(username='user', password='user')
        response = self.get("/auth/staff")
        assert response.status_code == 403

        self.client.login(username='staff', password='staff')
        response = self.get("/auth/staff")
        assert response.status_code == 200

        self.client.login(username='admin', password='admin')
        response = self.get("/auth/staff")
        assert response.status_code == 200

    def test_auth_token(self):
        user = User.objects.filter(username='user').first()

        response = self.get("/auth/authenticated")
        assert response.status_code == 401

        response = self.get("/auth/authenticated", X_API_KEY='test')
        assert response.status_code == 401

        token = user.assign_token()
        user.save()

        response = self.get("/auth/authenticated", X_API_KEY=f'{user.id}:2')
        assert response.status_code == 401

        response = self.get("/auth/authenticated", X_API_KEY=token)
        assert response.status_code == 200

    def test_json_security(self):
        with self.assertRaises(TypeError):
            response = self.get("/insecure")

    def test_json_handler(self):
        response = self.get('/bogus')
        assert response.status_code == 404
        assert response.data['message'] == "Not Found"

    def test_csrf_error(self):
        csrf_client = Client(enforce_csrf_checks=True)
        response = csrf_client.post('/csrf')
        assert response.status_code == 403
        assert response.data['message'] == "Permission Denied: CSRF Failure"

    def test_json_decode_error(self):
        assert self.client.post('/data', 'bogus!', content_type='application/json').json() == {}
