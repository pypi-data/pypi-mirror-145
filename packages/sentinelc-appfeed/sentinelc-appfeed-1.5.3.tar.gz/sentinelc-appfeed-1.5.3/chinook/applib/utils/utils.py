import datetime
from genericpath import isdir
from os import listdir
import re
import yaml
import collections
from .logger import eprint


def merge_dictionary(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = merge_dictionary(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def load_localized_yaml_file(path, app_name, lang, file_description):
    file = None
    file_path = f"{path}/{app_name}.yml"
    translation_path = f"{path}/{app_name}-{lang}.yml"

    try:
        with open(file_path, "r") as filestream:
            file = yaml.safe_load(filestream)
    except IOError:
        eprint(f"{file_description.capitalize()} '{file_path}'" + "could not be loaded.")
        return None

    if lang is not None:
        try:
            with open(translation_path, "r") as filestream:
                localized_file = yaml.safe_load(filestream)
                merge_dictionary(file, localized_file)
        except IOError:
            eprint(
                f"Warning  Localized {file_description} '{translation_path}'"
                + "could not be loaded. Language override will not be applied."
            )

    return file


def get_all_localization_files(path, file_name):
    file_name_no_ext = file_name.rsplit(".", 1)
    ext = file_name_no_ext[1]
    file_name_no_ext = file_name_no_ext[0]

    translation_files = {"en": f"{file_name}"}
    regexString = r"{file_name_no_ext}-([a-z]{{2,3}})\.{ext}".format(
        file_name_no_ext=file_name_no_ext, ext=ext
    )

    for file in listdir(f"{path}/"):
        if isdir(file):
            continue

        match = re.search(regexString, file)
        if match:
            translation_files[match.group(1)] = file

    return translation_files


def load_file_text(path, description):
    try:
        with open(path, "r") as filestream:
            return filestream.read()
    except IOError:
        eprint(f"{description.capitalize()} could not be loaded.")
        return None


def load_file_yaml(path, description):
    file_str = load_file_text(path, description)

    if file_str is None:
        return None

    loaded_file = None
    try:
        loaded_file = yaml.safe_load(file_str)
    except Exception:
        eprint(f"Yaml file format is invalid for file : '{path}'")

    return loaded_file


def get_localized_objects_yaml(path, app_name, description):
    data = {}
    locale_files = get_all_localization_files(path, f"{app_name}.yml")
    for locale in locale_files:
        data[locale] = load_file_yaml(f"{path}/{locale_files[locale]}", description)
    return data


def timestamp_to_json_string(timestamp):
    if not timestamp:
        return None
    event_datetime = datetime.datetime.utcfromtimestamp(int(timestamp))
    return "{0}Z".format(event_datetime.isoformat())
