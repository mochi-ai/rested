import pytest
from rested.validation import ValidationError, reject
from rested.validation.utils import Undefined
from rested.validation.validators.defined import defined
from rested.validation.validators.nonnull import nonnull
from rested.validation.validators.integer import integer
from rested.validation.validators.list import list
from rested.validation.validators.string import string
from rested.validation.validators.boolean import boolean
from rested.validation.validators.email import email
from rested.validation.validators.password import password
from rested.validation.validators.min import min
from rested.validation.validators.max import max
from rested.validation.validators.empty import empty
from rested.validation.validators.nonempty import nonempty
from rested.validation.validators.member import member


def test_defined(mocker):
    defined('bleh', reject=reject)
    with pytest.raises(ValidationError):
        defined(Undefined, reject=reject)

def test_nonnull(mocker):
    nonnull('bleh', reject=reject)
    with pytest.raises(ValidationError):
        nonnull(None, reject=reject)

def test_integer(mocker):
    integer(1, reject=reject)
    with pytest.raises(ValidationError):
        integer(None, reject=reject)

def test_list(mocker):
    list([], reject=reject)
    with pytest.raises(ValidationError):
        list(None, reject=reject)

def test_boolean(mocker):
    boolean(True, reject=reject)
    boolean(False, reject=reject)
    with pytest.raises(ValidationError):
        boolean(None, reject=reject)
    with pytest.raises(ValidationError):
        boolean('True', reject=reject)
    with pytest.raises(ValidationError):
        boolean(1, reject=reject)

def test_string(mocker):
    string("hello", reject=reject)
    with pytest.raises(ValidationError):
        string(None, reject=reject)

def test_email(mocker):
    email("stephen@hello.com", reject=reject)
    with pytest.raises(ValidationError):
        email("bogus@bogus", reject=reject)
    with pytest.raises(ValidationError):
        email("bogus", reject=reject)
    with pytest.raises(ValidationError):
        email("bogus.com", reject=reject)
    with pytest.raises(ValidationError):
        email(None, reject=reject)

def test_password(mocker):
    password("Changed123!", reject=reject)
    password("Hello123", reject=reject)
    with pytest.raises(ValidationError):
        password("a12345678", reject=reject) # no caps
    with pytest.raises(ValidationError):
        password("A12345678", reject=reject) # no lower
    with pytest.raises(ValidationError):
        password("aABCDEFGH", reject=reject) # no nums
    # with pytest.raises(ValidationError):
    #     password("Hello123", reject=reject)
    with pytest.raises(ValidationError):
        password("Hello1!", reject=reject)   # too short
    with pytest.raises(ValidationError):
        password("", reject=reject)
    with pytest.raises(ValidationError):
        password("", reject=reject)
    with pytest.raises(ValidationError):
        password(None, reject=reject)

def test_min(mocker):
    min(3)(3, reject=reject)
    min(2)("ab", reject=reject)
    min(2)([1, 2], reject=reject)
    with pytest.raises(ValidationError):
        min(3)(2, reject=reject)
    with pytest.raises(ValidationError):
        min(3)(0, reject=reject)
    with pytest.raises(ValidationError):
        min(2)("a", reject=reject)
    with pytest.raises(ValidationError):
        min(3)([1], reject=reject)

def test_max(mocker):
    max(3)(3, reject=reject)
    max(3)(0, reject=reject)
    max(2)("ab", reject=reject)
    max(2)("", reject=reject)
    max(2)([1], reject=reject)
    with pytest.raises(ValidationError):
        max(3)([1, 2, 3, 4], reject=reject)
    with pytest.raises(ValidationError):
        max(3)(4, reject=reject)
    with pytest.raises(ValidationError):
        max(2)("abc", reject=reject)

def test_empty(mocker):
    empty([], reject=reject)
    empty("", reject=reject)
    empty({}, reject=reject)
    empty(set(), reject=reject)
    with pytest.raises(ValidationError):
        empty([1], reject=reject)
    with pytest.raises(ValidationError):
        empty("a", reject=reject)
    with pytest.raises(ValidationError):
        empty({"a":1}, reject=reject)
    with pytest.raises(ValidationError):
        empty(set([1]), reject=reject)
    with pytest.raises(TypeError):
        empty(1, reject=reject)

def test_nonempty(mocker):
    with pytest.raises(ValidationError):
        nonempty([], reject=reject)
    with pytest.raises(ValidationError):
        nonempty("", reject=reject)
    with pytest.raises(ValidationError):
        nonempty({}, reject=reject)
    with pytest.raises(ValidationError):
        nonempty(set(), reject=reject)
    nonempty([1], reject=reject)
    nonempty("a", reject=reject)
    nonempty({"a":1}, reject=reject)
    nonempty(set([1]), reject=reject)
    with pytest.raises(TypeError):
        nonempty(1, reject=reject)

def test_membership(mocker):
    member([1, 2, 3])(1, reject=reject)
    member([1, 2])(2, reject=reject)
    member(['a'])('a', reject=reject)
    member(set([1, 2]))(1, reject=reject)
    member({'a': 9})('a', reject=reject)
    member({'z': 9})('z', reject=reject)
    with pytest.raises(ValidationError):
        member([1, 2, 3])(4, reject=reject)
    with pytest.raises(ValidationError):
        member(set([1]))('a', reject=reject)
    with pytest.raises(ValidationError):
        member('xz')('a', reject=reject)
