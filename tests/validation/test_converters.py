import pytest
from rested.validation import ValidationError, reject
from rested.validation.converters.integer import integer
from rested.validation.converters.string import string
from rested.validation.converters.boolean import boolean
from rested.validation.converters.model import model
from example.models import Person


def test_integer():
    assert integer("123") == 123
    assert integer(123) == 123

def test_string():
    assert string(123) == "123"
    assert string("123") == "123"

def test_boolean():
    assert boolean(0) == False
    assert boolean(1) == True
    assert boolean("false") == False
    assert boolean("true") == True
    assert boolean("False") == False
    assert boolean("True") == True

def test_model(db):
    billy = Person.objects.create(name="billy").save()
    susan = Person.objects.create(name="susan").save()

    assert billy == model(Person)(billy.id, reject=reject)
    assert billy == model(Person, 'name')('billy', reject=reject)
    assert susan == model(Person, 'name')('susan', reject=reject)

    with pytest.raises(ValidationError):
        model(Person)(99, reject=reject)
    with pytest.raises(ValidationError):
        model(Person, 'name')('david hilbert', reject=reject)
    with pytest.raises(ValidationError):
        model(Person)(None, reject=reject)
    with pytest.raises(ValidationError):
        model(Person)(None, 'bogus', reject=reject)
