import os

import pytest

from chinook.applib.builder import build_feed
from chinook.applib.utils.exceptions import ValidationError

BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data"


def test_ports_valids():
    build_feed(f"{BASEPATH}/ports_valid")


def test_invalid_protocol():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/port_invalid_protocol")


def test_invalid_port_number_lw():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/port_invalid_number_lw")


def test_invalid_port_number_gt():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/port_invalid_number_gt")


def test_invalid_expose():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/port_invalid_expose")


def test_invalid_duplicate_port():
    with pytest.raises(ValidationError):
        build_feed(f"{BASEPATH}/invalid_duplicate_port")


def test_valid_duplicate_port():
    build_feed(f"{BASEPATH}/valid_duplicate_port")
