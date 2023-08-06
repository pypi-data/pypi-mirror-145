import pytest

from chinook.applib.validator import validate_kube_yaml, ValidationError

MULTIPLE_DOCUMENTS = """
apiVersion: v1
kind: Pod
metadata:
  name: test2
spec:
  containers:
  - command:
    - bash
    image: docker.io/library/ubuntu:latest
status: {}
---
metadata:
  creationTimestamp: null
spec: {}
status:
  loadBalancer: {}
"""

SINGLE_DOCUMENT = """
apiVersion: v1
kind: Pod
metadata:
  name: test2
spec:
  containers:
  - command:
    - bash
    image: docker.io/library/ubuntu:latest
status: {}
"""


def test_multiple_documents_are_rejected():
    with pytest.raises(ValidationError) as ex_info:
        validate_kube_yaml(MULTIPLE_DOCUMENTS, "fakepath.yml")

    assert (
        str(ex_info.value)
        == "Kube yaml must contain a single document: fakepath.yml. Remove the --- footer."
    )


def test_single_documents_are_accepted():
    assert validate_kube_yaml(SINGLE_DOCUMENT, "fakepath.yml") is None
