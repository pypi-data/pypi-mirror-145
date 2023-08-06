from chinook.applib.builder import build_feed

MANIFESTS = "tests/version_order/data/manifests/"


def test_version_order():
    feed = build_feed(MANIFESTS)

    app_versions = feed["apps"][0].get("versions")
    version_strings = [version["infos"]["version"] for version in app_versions]

    assert version_strings == [
        "0.0.1",
        "0.0.1-r0",
        "1.0.0",
        "2.0.1",
        "2.0.1-r0",
        "2.0.1b",
        "2.2.0",
        "2.10.0",
        "10.0.0",
        "latest",
    ]
