import pytest

def revers_string(input):
    return input[::-1]

def test_my_first_test():
    assert "TestingIsFun" == revers_string("nuFsIgnitseT")