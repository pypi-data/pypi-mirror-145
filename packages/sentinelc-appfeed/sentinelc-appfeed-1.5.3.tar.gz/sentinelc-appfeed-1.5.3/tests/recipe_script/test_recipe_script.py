import os
from shutil import rmtree

from chinook.applib.recipe import create_folder

BASEFOLDER = os.getcwd()
DEFAULT_MANIFEST = "manifests"
APP_NAME = "test"

MANIFEST = f"{BASEFOLDER}/{DEFAULT_MANIFEST}"
APP = f"{MANIFEST}/{APP_NAME}"


def setUp():
    tearDown()
    os.mkdir(MANIFEST)


def tearDown():
    rmtree(MANIFEST, ignore_errors=True)


def verify_architecture(version):
    # Check if root exist
    assert os.path.isdir(APP)

    # Check if description files exists
    assert os.path.isfile(f"{APP}/README.md")
    assert os.path.isfile(f"{APP}/README-fr.md")
    assert os.path.isfile(f"{APP}/{APP_NAME}.yml")
    assert os.path.isfile(f"{APP}/{APP_NAME}-fr.yml")

    # check if version folder exist
    assert os.path.isdir(f"{APP}/versions")
    version_folder = f"{APP}/versions/{version}"
    assert os.path.isdir(version_folder)

    # Check if version files exist
    assert os.path.isfile(f"{version_folder}/{APP_NAME}_{version}.yml")
    assert os.path.isfile(f"{version_folder}/{APP_NAME}_{version}-fr.yml")
    assert os.path.isfile(f"{version_folder}/{APP_NAME}_{version}.kube.yml")


def test_recipe_creation():
    setUp()
    create_folder(MANIFEST, APP_NAME, "0.0.1")
    verify_architecture("0.0.1")
    tearDown()


def test_bump_version():
    setUp()
    create_folder(MANIFEST, APP_NAME, "0.0.1")
    verify_architecture("0.0.1")

    create_folder(MANIFEST, APP_NAME, "0.0.2", "0.0.1")
    verify_architecture("0.0.2")
    tearDown()
