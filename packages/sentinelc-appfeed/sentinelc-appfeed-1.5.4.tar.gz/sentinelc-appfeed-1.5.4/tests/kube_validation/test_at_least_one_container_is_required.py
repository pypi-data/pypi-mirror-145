import pytest

from chinook.applib.validator import validate_kube_yaml, ValidationError

MISSING_CONTAINERS = """
apiVersion: v1
kind: Pod
metadata:
  name: test2
spec:
  junk: is no good
status: {}
"""

EMPTY_CONTAINERS = """
apiVersion: v1
kind: Pod
metadata:
  name: test2
spec:
  containers:
status: {}
"""

ONE_CONTAINERS = """
apiVersion: v1
kind: Pod
metadata:
  name: test2
spec:
  containers:
  - image: docker.io/library/hello-world:latest
    name: hello-world
status: {}
"""

TWO_CONTAINERS = """
apiVersion: v1
kind: Pod
metadata:
  name: test2
spec:
  containers:
  - image: docker.io/library/hello-world:latest
    name: hello-world
  - image: docker.io/library/hello-world:latest
    name: hello-world2
status: {}
"""


def test_at_least_one_container():
    with pytest.raises(ValidationError) as ex_info:
        validate_kube_yaml(MISSING_CONTAINERS, "fakepath.yml")
    assert str(ex_info.value) == "fakepath.yml: missing or invalid containers"

    with pytest.raises(ValidationError) as ex_info:
        validate_kube_yaml(EMPTY_CONTAINERS, "fakepath.yml")
    assert str(ex_info.value) == "fakepath.yml: missing or invalid containers"

    assert validate_kube_yaml(ONE_CONTAINERS, "fakepath.yml") is None
    assert validate_kube_yaml(TWO_CONTAINERS, "fakepath.yml") is None
