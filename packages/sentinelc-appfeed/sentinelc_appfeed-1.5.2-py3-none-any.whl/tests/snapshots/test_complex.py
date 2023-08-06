import json

from chinook.applib.builder import build_feed

MANIFESTS = "tests/snapshots/data/complex/manifests/"
EXPECTED = "tests/snapshots/data/complex/expected-output.json"


def test_snapshot_complex():
    apps = build_feed(MANIFESTS)
    expected = json.loads(open(EXPECTED).read())
    assert apps == expected
