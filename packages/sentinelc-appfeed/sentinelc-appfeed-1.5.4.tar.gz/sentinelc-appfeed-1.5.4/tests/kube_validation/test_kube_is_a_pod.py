import pytest
from chinook.applib.validator import ValidationError, validate_kube_yaml

INVALID = """
apiVersion: v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
"""

VALID = """
apiVersion: v1
kind: Pod
metadata:
  name: hello-world
spec:
  containers:
  - image: docker.io/library/hello-world:latest
    name: hello-world
status: {}

"""


MISSING_API_VERSION = """
kind: Pod
metadata:
  name: hello-world
spec:
  containers:
  - image: docker.io/library/hello-world:latest
    name: hello-world
status: {}

"""


def test_non_pods_are_rejected():
    with pytest.raises(ValidationError) as ex_info:
        validate_kube_yaml(INVALID, "fakepath.yml")

    assert str(ex_info.value) == "fakepath.yml: kind must be Pod"


def test_api_version_is_required():
    with pytest.raises(ValidationError) as ex_info:
        validate_kube_yaml(MISSING_API_VERSION, "fakepath.yml")

    assert str(ex_info.value) == "fakepath.yml: apiVersion must be v1"


def test_pods_are_accepted():
    assert validate_kube_yaml(VALID, "fakepath.yml") is None
