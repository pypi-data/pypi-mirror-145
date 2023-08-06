import os

import pytest
from chinook.applib.builder import build_feed

from chinook.applib.validator import ValidationError


BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data"


def test_validate_auto_immutable():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/auto_mutable")


def test_validate_reveal_not_secret():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/reveal_not_secret")


def test_valid_types():
    build_feed(f"{BASEPATH}/types/valid")


def test_invalid_type():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/types/invalid")


def test_empty_regexp():
    build_feed(f"{BASEPATH}/regexp/valid")


def test_valid_regexp():
    build_feed(f"{BASEPATH}/regexp/valid")


def test_invalid_regexp():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/regexp/invalid")
