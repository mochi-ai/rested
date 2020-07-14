import pytest
from rested.test.fixtures import database
# pytestmark = pytest.mark.django_db


db = database(reset_sequences=False, autouse=True)

def test_ping(rest):
    response = rest.get('/ping')
    assert response.status == 200
    assert response.data == {"data": "pong"}
