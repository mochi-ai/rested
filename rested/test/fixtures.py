import pytest
from functools import wraps


def database(transactional=False, reset_sequences=False, autouse=True):
    from pytest_django.fixtures import _django_db_fixture_helper as helper
    @pytest.fixture(autouse=autouse)
    def db(request, django_db_setup, django_db_blocker):
        if reset_sequences: assert transactional, "Reset sequences only works when transactional is True."
        helper(request, django_db_blocker, transactional=transactional, reset_sequences=reset_sequences)
    return db

def authenticated_rest_client(autouse=True):
    @pytest.fixture(autouse=True)
    def authenticated_rest_client_fixture(rest, user):
        def inject_api_token(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                kwargs['HTTP_X_API_KEY'] = user._token
                return f(*args, **kwargs)
            return wrapped

        rest.get = inject_api_token(rest.get)
        rest.put = inject_api_token(rest.put)
        rest.post = inject_api_token(rest.post)
        rest.delete = inject_api_token(rest.delete)
        return rest
    return authenticated_rest_client_fixture

@pytest.fixture()
def rest():
    from rested.test import Client
    return Client()
