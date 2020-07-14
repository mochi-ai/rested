import pytest


def database(transactional=False, reset_sequences=False, autouse=True):
    from pytest_django.fixtures import _django_db_fixture_helper as helper
    @pytest.fixture(autouse=autouse)
    def db(request, django_db_setup, django_db_blocker):
        if reset_sequences: assert transactional, "Reset sequences only works when transactional is True."
        helper(request, django_db_blocker, transactional=transactional, reset_sequences=reset_sequences)
    return db

@pytest.fixture()
def rest():
    from rested.test import Client
    return Client()
