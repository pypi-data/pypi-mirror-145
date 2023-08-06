import os

import pytest
from chinook.applib.builder import build_feed

from chinook.applib.validator import ValidationError


BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data/variable_mapping"


def test_variable_set():
    build_feed(f"{BASEPATH}/variable-set")


def test_variable_missing_template():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/variable-missing")


def test_variable_missing():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/template-missing")
