import argparse
from natsort import natsorted
from os import listdir
import os
import sys
import re
from jinja2 import Template, Undefined, Environment, meta
from humanfriendly import InvalidSize, parse_size

import yaml

from .utils.ArgparseCustomTypes import ArgparseCustomTypes

from .utils.exceptions import ValidationError
from .utils.logger import eprint

from .utils.utils import (
    get_all_localization_files,
    get_localized_objects_yaml,
    load_file_text,
    timestamp_to_json_string,
)

description_translatable_fields = ["display_name", "description"]

mandatory_description_fields = [
    "display_name",
    "description",
    "category",
]

description_defaults = {"homepage": "", "documentation": ""}

recipe_translatable_fields = ["label", "description"]

recipe_variables_defaults = {
    "type": "text",
    "required": False,
    "regexp": None,
    "default": "",
    "auto": False,
    "secret": False,
    "immutable": False,
    "reveal_once": False,
}

recipe_ports_defaults = {
    "protocol": "TCP",
    "description": None,
    "expose_vlan": "false",
    "expose_cloud": "never",
}

expose_values = {"true", "false", "never"}

port_protocol_values = {"TCP", "UDP"}

ports_translatable_fields = ["description"]

accepted_variable_types = {"text", "checkbox", "number", "password", "email", "url", "textarea"}

requirement_defaults = {"storage": None, "memory": None}


def parse_versions(app_path, app_name):
    versions = []
    for version_string in listdir(f"{app_path}/versions"):
        # validate
        if not re.search(r"([a-z0-9\.\-]+?)(-r([0-9]+))?$", version_string):
            raise ValidationError(
                """
Version name is invalid.
It must be alphanumeric and includes dash and dots.
A revision can be attached with -r and the number of the revision.
            """
            )

        versions.append(parse_single_version(app_path, app_name, version_string))

    return versions


def parse_single_version(app_path, app_name, version_string):
    eprint(f" --version: {version_string}")
    version_path = f"{app_path}/versions/{version_string}"
    main_version_file = f"{version_path}/{app_name}_{version_string}.yml"

    # Get all localisations
    version_files = get_localized_objects_yaml(
        version_path,
        f"{app_name}_{version_string}",
        "version description file",
    )
    if version_files.get("en") is None:
        raise ValidationError(f"The main version file could not be loaded: {main_version_file}")

    version = version_files["en"]
    del version_files["en"]

    # localize
    if "vars" in version:
        for var in version["vars"]:
            for key in recipe_translatable_fields:
                if key in version["vars"][var]:
                    version["vars"][var][key] = {"en": version["vars"][var][key]}
                else:
                    version["vars"][var][key] = {}

        for locale in version_files:
            current_locale = version_files[locale]
            for var in version["vars"]:
                if var in current_locale["vars"]:
                    for key in recipe_translatable_fields:
                        if key in current_locale["vars"][var]:
                            version["vars"][var][key][locale] = current_locale["vars"][var][key]

    else:
        version["vars"] = {}

    if "ports" in version:
        for port in version["ports"]:
            for key in ports_translatable_fields:
                if key in version["ports"][port]:
                    version["ports"][port][key] = {"en": version["ports"][port][key]}
                else:
                    version["ports"][port][key] = {}

        for locale in version_files:
            current_locale = version_files[locale]
            for port in version["ports"]:
                if port in current_locale["ports"]:
                    for key in ports_translatable_fields:
                        if key in current_locale["ports"][port]:
                            version["ports"][port][key][locale] = current_locale["ports"][port][key]
    else:
        version["ports"] = {}

    # Validate infos
    if "infos" not in version:
        version["infos"] = {}

    # Adds archs default
    if "architectures" not in version["infos"]:
        version["infos"]["architectures"] = []

    # validate requirements
    if "requirements" not in version["infos"]:
        version["infos"]["requirements"] = {}

    # adds defaults
    for key in requirement_defaults:
        if key not in version["infos"]["requirements"]:
            version["infos"]["requirements"][key] = requirement_defaults[key]

    for key in version["infos"]["requirements"]:
        cur_requirement = version["infos"]["requirements"][key]
        if cur_requirement is not None:
            size = None
            try:
                size = parse_size(cur_requirement, False)
            except InvalidSize:
                raise ValidationError(
                    f"Requirement {key} in {app_name}_{version_string} is not parsable"
                )
            version["infos"]["requirements"][key] = size

    # Variable based validation
    for key in version["vars"]:
        var = version["vars"][key]

        # Adds defaults
        for option, default in recipe_variables_defaults.items():
            if option not in var:
                var[option] = default

        # Block posibility of an automatic,mutable variable
        if var["auto"] and not var["immutable"]:
            raise ValidationError(f"{key} in App {app_name} can't be automatic and mutable")

        # Block posibility of an reveal_once other if the variable is not secret
        if var["reveal_once"] and not var["secret"]:
            raise ValidationError(
                f"{key} in App {app_name} doesn't need to be revealed_once if not secret"
            )

        if var["type"] not in accepted_variable_types:
            raise ValidationError(f"{key} in App {app_name} contains an invalid type")

        if "regexp" in var and var["regexp"] is not None:
            try:
                re.compile(var["regexp"])
            except re.error:
                raise ValidationError(
                    f"{key} in App {app_name} contains an invalid regular expression"
                )

    # port based validation
    used_ports = {}
    for key in version["ports"]:
        port = version["ports"][key]

        # Adds defaults
        for option, default in recipe_ports_defaults.items():
            if option not in port:
                port[option] = default

        if port["port"] is None:
            raise ValidationError(
                f"port {key} in App {app_name} must have a port number between 1 and 65535"
            )

        port_number = int(port["port"])
        if not 1 <= port_number <= 65535:
            raise ValidationError(
                f"port {key} in App {app_name} must have a port number between 1 and 65535"
            )

        if port["protocol"] not in port_protocol_values:
            raise ValidationError(f"port {key} in App {app_name} protocol is invalid ('TCP','UDP')")

        if port["expose_vlan"] not in expose_values:
            raise ValidationError(
                f"port {key} in App {app_name} vlan exposition is invalid ('true','false','never')"
            )

        if port["expose_cloud"] not in expose_values:
            raise ValidationError(
                f"port {key} in App {app_name} vlan exposition is invalid ('true','false','never')"
            )

        current_port = port["port"]
        current_protocol = port["protocol"]

        if (
            current_port in used_ports
            and current_protocol in used_ports[current_port]
            and used_ports[current_port][current_protocol]
        ):
            raise ValidationError(
                f"port {key} in App {app_name} is a duplicated port number and protocol"
            )

        # Adds it to the check
        if current_port not in used_ports:
            used_ports[current_port] = {"TCP": False, "UDP": False}
        used_ports[port["port"]][port["protocol"]] = True

    # Adds last commit
    timestamp = os.popen(f"git log --format=%ct {main_version_file}").read()
    timestamp = timestamp[:-1]
    version["infos"]["publish_date"] = timestamp_to_json_string(timestamp.split("\n")[-1])

    # Adds version
    version["infos"]["version"] = version_string

    # Adds kube
    kube_yml_filename = f"{version_path}/{app_name}_{version_string}.kube.yml"
    kube_string = load_file_text(
        kube_yml_filename,
        "kubernetes template file",
    )

    # Validate parameter parity
    env = Environment()
    parsed_template = env.parse(kube_string)
    template_vars_list = meta.find_undeclared_variables(parsed_template)

    var_list = version["vars"].keys()

    if template_vars_list != var_list:
        error_str = ""
        if len(template_vars_list) > len(var_list):
            error_str = (
                f"Some variables set in the template of the App {app_name}_{version_string} "
            )
            error_str += "does not have a definition : \n"
            dif = template_vars_list - var_list
        else:
            error_str = "Some variables are defined but not found in the template of "
            error_str += f"{app_name}_{version_string} : \n"
            dif = var_list - template_vars_list

        for var in dif:
            error_str += f"- {var}"
        raise ValidationError(error_str)

    validate_kube_yaml(kube_string, kube_yml_filename)

    version["kube"] = kube_string

    eprint(" ---- VALID ----")
    return version


def validate(manifest_path, app_name):
    bail_on_shallow_git_repos()
    path = f"{manifest_path}/{app_name}"

    # Validate App Name
    app_name = path.split("/")[-1]
    eprint(f"Now validating {app_name}")

    match = re.search(r"(^[a-z0-9\-]+$)", app_name)
    if not match:
        raise ValidationError(f"Invalid app name: {app_name}")

    # Get App Infos
    app_files = get_localized_objects_yaml(path, app_name, "description file")

    if app_files["en"] is None:
        raise ValidationError(
            f"The main description file could not be loaded : {path}/{app_name}.yml"
        )

    app = app_files["en"]
    del app_files["en"]

    app["name"] = app_name

    for field in description_translatable_fields:
        if field in app:
            app[field] = {"en": app[field]}

    for locale in app_files:
        current_app_file = app_files[locale]
        for field in description_translatable_fields:
            if field in current_app_file:
                app[field][locale] = current_app_file[field]

    # Get full descriptions
    if "full_description" not in app:
        app["full_description"] = {}
    readmes = get_all_localization_files(path, "README.md")

    for locale in readmes:
        current_readme = load_file_text(f"{path}/{readmes[locale]}", "readme file")
        app["full_description"][locale] = current_readme

    # Get versions
    versions = parse_versions(path, app_name)
    if not versions:
        raise ValidationError(f"App {app_name} does not contain any versions")

    versions = natsorted(versions, key=lambda x: x["infos"]["version"])
    app["versions"] = versions

    # Check for mandatory fields
    has_mandatory_fields = True
    for field in mandatory_description_fields:
        if field not in app:
            if field in description_translatable_fields:
                if app[field]["en"] is None:
                    has_mandatory_fields = False
                    eprint(f"Mandatory field '{field}' from app '{app_name}' is missing")
            else:
                has_mandatory_fields = False
                eprint(f"Mandatory field '{field}' from app '{app_name}' is missing")

    for field in description_defaults:
        if field not in app:
            app[field] = description_defaults[field]

    # Return object if valid
    if not has_mandatory_fields:
        raise ValidationError(f"App {app_name} is invalid: Missing mandatory field(s)")

    eprint(f"App {app_name} is valid")
    return app


def replace_jinja_values(kube_string):
    return Template(kube_string, undefined=Undefined).render()


def validate_kube_yaml(kube_string, filepath):
    if not kube_string:
        raise ValidationError(f"No kube file found : {filepath}")

    validation_kube_string = replace_jinja_values(kube_string)

    if not kube_yaml_is_single_document(validation_kube_string):
        raise ValidationError(
            f"Kube yaml must contain a single document: {filepath}. Remove the --- footer."
        )

    kube_document = yaml.safe_load(validation_kube_string)

    error = (
        kube_yaml_has_basic_fields(kube_document)
        or kube_yaml_has_at_least_one_container(kube_document)
        or kube_yaml_has_no_status(kube_document)
    )
    if error:
        raise ValidationError(f"{filepath}: {error}")


def kube_yaml_is_single_document(kube_string):
    try:
        yaml.safe_load(kube_string)
        return True
    except yaml.composer.ComposerError:
        return False


def kube_yaml_has_basic_fields(kube_document):
    if kube_document.get("apiVersion") != "v1":
        return "apiVersion must be v1"
    if kube_document.get("kind") != "Pod":
        return "kind must be Pod"


def kube_yaml_has_at_least_one_container(kube_document):
    spec = kube_document.get("spec")
    if type(spec) != dict:
        return "missing or invalid spec"

    containers = spec.get("containers")
    if type(containers) != list:
        return "missing or invalid containers"

    if len(containers) == 0:
        return "should define at least one container"


def kube_yaml_has_no_status(kube_document):
    status = kube_document.get("status")
    if status or status != {}:
        return "should not define a status"


def bail_on_shallow_git_repos():
    is_shallow = os.popen("git rev-parse --is-shallow-repository").read()[:-1]
    if is_shallow == "true":
        eprint(
            "You appear to be running in a shallow git clone. This script uses the "
            "git log command to get commit dates of your packages and will fail in a "
            "shallow clone."
        )
        eprint(
            "If you are using gitlab-ci, set the Git shallow clone settings to 0"
            + " in your project's CI:CD settings."
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="""
        Validates the folder hiearchy and values of a specific app in the manifest
                
        how to use
        ------------
        `applib-recipe newapp`
        Validates the `newapp` app located inside the ./manifests folder
        
        `applib-recipe -p newmanifest newapp`
        Validates the `newapp` app located inside the ./newmanifest folder
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
        "app_name",
        action="store",
        help="Specify the name of the app to validate.",
    )

    args = parser.parse_args()

    validate(args.path, args.app_name)


if __name__ == "__main__":
    main()
