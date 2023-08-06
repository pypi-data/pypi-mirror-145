import os
from chinook.applib.builder import build_feed

BASEPATH = f"{os.path.dirname(os.path.abspath(__file__))}/data"


def test_values_should_be_null():
    feed = build_feed(f"{BASEPATH}/empty")
    app_version = feed["apps"][0]["versions"][0]
    assert app_version["infos"]["requirements"]["storage"] is None
    assert app_version["infos"]["requirements"]["memory"] is None


def test_requirements_contains_values():
    feed = build_feed(f"{BASEPATH}/contain-values")
    app_version = feed["apps"][0]["versions"][0]
    assert app_version["infos"]["requirements"]["storage"] == 1000000000
    assert app_version["infos"]["requirements"]["memory"] == 500000000
