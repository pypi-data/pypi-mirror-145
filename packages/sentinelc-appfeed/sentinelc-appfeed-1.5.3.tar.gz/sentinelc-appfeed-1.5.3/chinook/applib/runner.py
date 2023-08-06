import argparse
from collections import namedtuple
import time

from chinook.applib.utils.exceptions import ValidationError

from .utils.ArgparseCustomTypes import ArgparseCustomTypes

from .utils.utils import load_file_text
from .validator import parse_single_version
import jinja2


def create_launch_script(template, substitution):
    return jinja2.Template(template).render(**substitution)


def get_localised_attr(c, attr, lang):
    value = ""
    if hasattr(c, attr):
        attr_idx = c._fields.index(attr)
        field = c[attr_idx]
        if "en" in field:
            value = field["en"]
        if lang in field:
            value = field[lang]
    return value


def getVariableValues(configs, lang, use_defaults):
    substitution = {}
    if "vars" not in configs:
        configs["vars"] = []

    for key in configs["vars"]:
        c = namedtuple("config", configs["vars"][key].keys())(*configs["vars"][key].values())

        if use_defaults:
            if c.default is not None:
                substitution[key] = c.default
            else:
                raise ValidationError(f"Variable {key} has no default value")
        else:
            type = c.type if hasattr(c, "type") else "text"
            default = c.default if hasattr(c, "default") else ""
            description = get_localised_attr(c, "description", lang)
            label = get_localised_attr(c, "label", lang)

            print(f"@ key: {key} - type: {type} - default value : {default} - {description}")
            print(f"Input the entry for {label} :")
            terminal_input = input()

            if hasattr(c, "default") and terminal_input == "":
                terminal_input = c.default
            substitution[key] = terminal_input

    return substitution


def run_pod(manifest_path, app_name, version, lang, output_folder, use_defaults):
    path = f"{manifest_path}/{app_name}"
    kube_file_path = f"{path}/versions/{version}/{app_name}_{version}.kube.yml"
    template = load_file_text(kube_file_path, "Kube description file")

    configs = parse_single_version(path, app_name, version)

    substitution = getVariableValues(configs, lang, use_defaults)
    launch_script = create_launch_script(template, substitution)

    file_name = f"{app_name}_{time.time()}.yml"

    with open(f"{output_folder}/{file_name}", "w") as outfile:
        outfile.write(launch_script)


def main():
    parser = argparse.ArgumentParser(
        description="""
        Creates a Yaml file that can be 'run with podman using "podman play kube {file}"'
        
        how to use
        ------------
        `applib-runner newapp 1.0`
        Prompts through all parameters of the app `newapp` app version 1.0 located inside the ./manifest folder
        then create the kubernete config file ./out/newapp{timestamp}

        `applib-runner newapp 1.1 -p newmanifest -o newout -l fr`
        Prompts through all parameters of the `newapp` app version 1.1, using french translations, located inside the ./newmanifest folder
        then create the kubernete config file ./newout/newapp{timestamp}
        
        `applib-runner newapp 1.0 -d`
        Creates the kubernete config file ./out/newapp{timestamp} using the default value of each parameter.
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

    parser.add_argument("app_name", action="store", help="Specify the name of the app to run.")

    parser.add_argument(
        "version",
        action="store",
        help='Specify the Folder inside the version file of the specified app. Example: "1.0.0"',
    )

    parser.add_argument(
        "-o",
        "--out",
        action="store",
        help='Specify the output Folder for the Yaml file. Default: "./out"',
        type=ArgparseCustomTypes.dir_path,
        default="./out",
    )

    parser.add_argument(
        "-l",
        "--lang",
        action="store",
        help="Specify the language override. Default: None (English)",
        default=None,
        nargs="?",
    )

    parser.add_argument(
        "-d",
        "--use-defaults",
        action=argparse.BooleanOptionalAction,
        help="Use default values to create kube yaml",
        default=False,
    )

    args = parser.parse_args()

    run_pod(args.path, args.app_name, args.version, args.lang, args.out, args.use_defaults)


if __name__ == "__main__":
    main()
