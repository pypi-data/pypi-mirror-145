import argparse
from os import makedirs
import os
from shutil import copytree

from chinook.applib.utils.ArgparseCustomTypes import ArgparseCustomTypes


def create_folder(path, name, version, older_version=None):

    # creates base folder
    path = os.path.realpath(path)
    makedirs(path, exist_ok=True)

    # set app absolute folder
    app_path = os.path.join(path, name)
    version_path = app_path + "/versions/" + version

    if older_version is not None:
        older_version_path = app_path + "/versions/" + older_version
        copytree(older_version_path, version_path)
    else:
        template_path = os.path.dirname(__file__) + "/template"
        copytree(template_path, app_path)
        os.rename(f"{app_path}/versions/1.0.0", f"{app_path}/versions/{version}")
        set_app_name(app_path, name, version)
        older_version = "1.0.0"

    set_version_number(version_path, version, older_version)


def replace_name_files(folder, str, substitution):
    for item in os.listdir(folder):
        if os.path.isfile:
            new_name = item.replace(str, substitution)
            os.rename(f"{folder}/{item}", f"{folder}/{new_name}")


def set_app_name(app_path, name, version):
    replace_name_files(app_path, "template", name)
    replace_name_files(f"{app_path}/versions/{version}", "template", name)


def set_version_number(version_path, version, old_version):
    replace_name_files(version_path, old_version, version)


def main():
    parser = argparse.ArgumentParser(
        description="""
        Create a recipe, either using a template or an older version of the app

        how to use
        ------------
        `applib-recipe newapp 1.0`
        Creates an app called newapp inside the ./manifests folder with a version folder 1.0 that use our app template

        `applib-recipe -p newmanifest newapp 1.0`
        Creates an app called newapp inside the ./newmanifest folder with a version folder 1.0 that use our app template

        `applib-recipe -p newmanifest newapp 1.1 -f 1.0`
        Creates a new version of the app `newapp` inside the ./newmanifest folder with a version folder 1.1 that use the version 1.0 as a base
        """  # noqa: W293 E501
    )

    parser.add_argument(
        "-p",
        "--path",
        action="store",
        help='Specify the root of the manifest folder. Default: "./manifests"',
        type=ArgparseCustomTypes.dir_path,
        default="./manifests",
    )

    parser.add_argument(
        "name",
        action="store",
        help="Specify the name of the app",
    )

    parser.add_argument(
        "version",
        action="store",
        help="Specify the name of the version",
    )

    parser.add_argument(
        "-f",
        "--fromVersion",
        action="store",
        help="Specify the name of the version to base the new version",
    )

    args = parser.parse_args()

    create_folder(args.path, args.name, args.version, args.fromVersion)


if __name__ == "__main__":
    main()
