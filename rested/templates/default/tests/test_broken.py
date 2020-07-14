import pytest

@pytest.mark.skip
def test_fail():
    assert True == False

@pytest.mark.skip
def test_fail_again():
    assert True == False
