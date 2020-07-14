from rested.validation.utils import Undefined
from rested.validation.acceptors.any import any
from rested.validation.acceptors.null import null
from rested.validation.acceptors.undefined import undefined


def test_any(mocker):
    accept = mocker.Mock()
    test = any(['a', 'b'])
    null('bleh', accept)
    assert not accept.called
    test('a', accept)
    assert accept.called
    test('b', accept)
    assert accept.call_count == 2

def test_null(mocker):
    accept = mocker.Mock()
    null('bleh', accept)
    assert not accept.called
    null(None, accept)
    assert accept.called

def test_undefined(mocker):
    accept = mocker.Mock()
    undefined('bleh', accept)
    assert not accept.called
    undefined(Undefined, accept)
    assert accept.called
