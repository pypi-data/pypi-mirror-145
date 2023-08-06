import argparse
from genericpath import isfile
import json
from os import listdir

from .utils.ArgparseCustomTypes import ArgparseCustomTypes

from .validator import validate

version = 1


def build_feed(manifest_path):
    apps = []

    # List valid apps
    for folder in listdir(manifest_path):
        item = f"{manifest_path}/{folder}"
        if isfile(item):
            continue
        app = validate(manifest_path, folder)

        if app is not None:
            apps.append(app)

    # sort
    apps.sort(key=lambda x: x["name"])

    feed = {"version": version, "apps": apps}

    return feed


def main():

    parser = argparse.ArgumentParser(
        description="""
        Creates a JSON file containing the valid apps located inside the manifest folder

        how to use
        -------------

        `applib-builder`
        Creates a feed based on the ./manifest folder and output the feed as ./feed/demo-feed.yml

        `applib-builder -p newmanifest -o customfeed -f feed.yml`
        Creates a feed based on the ./newmanifest folder and output the feed as ./customfeed/feed.yml
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
        "-o",
        "--out",
        action="store",
        help='Specify the output Folder for the JSON file. Default: "./feeds"',
        type=ArgparseCustomTypes.dir_path,
        default="./feeds",
    )

    parser.add_argument(
        "-f",
        "--filename",
        action="store",
        help='Specify the name of the output file. Default: "demo-feed"',
        default="demo-feed",
    )

    args = parser.parse_args()

    feed = build_feed(args.path)

    with open(f"{args.out}/{args.filename}.json", "w") as outfile:
        json.dump(feed, outfile, indent=4)


if __name__ == "__main__":
    main()
