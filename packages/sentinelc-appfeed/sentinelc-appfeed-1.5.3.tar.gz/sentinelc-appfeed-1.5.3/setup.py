import os
import setuptools

if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('CI_JOB_ID'):
    version = os.environ['CI_JOB_ID']
else:
    version = "dev"

setuptools.setup(
    name="sentinelc-appfeed",
    version=version,
    url="https://gitlab.sentinelc.com/sentinel-c/app-library-builder",
    maintainer="Sentinel-C",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "applib-builder = chinook.applib.builder:main",
            "applib-validator = chinook.applib.validator:main",
            "applib-runner = chinook.applib.runner:main",
            "applib-recipe = chinook.applib.recipe:main"
        ]
    },
    install_requires=[
        "argparse",
        "PyYAML",
        "humanfriendly",
        "jinja2",
        "natsort"
    ],
    include_package_data=True,
)
