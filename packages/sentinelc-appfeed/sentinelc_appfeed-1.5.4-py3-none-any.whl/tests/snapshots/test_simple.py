import json

from chinook.applib.builder import build_feed

MANIFESTS = "tests/snapshots/data/simple/manifests/"
EXPECTED = "tests/snapshots/data/simple/expected-output.json"


def test_snapshot_simple():
    apps = build_feed(MANIFESTS)
    expected = json.loads(open(EXPECTED).read())
    assert apps == expected
