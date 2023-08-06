#!/usr/bin/env python

import importlib.util
import os
from pathlib import Path

from setuptools import find_packages, setup


def read_flowcontrol_version():
    """This reads the version from omnetinireader/version.py without importing parts of
    reder (which would require some of the dependencies already installed)."""
    # code parts were taken from here https://stackoverflow.com/a/67692

    path2setup = os.path.dirname(__file__)
    version_file = os.path.abspath(
        os.path.join(path2setup, "omnetinireader", "version.py")
    )

    spec = importlib.util.spec_from_file_location("version", version_file)
    version = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(version)
    return version.Version.v_short


# see documentation
# https://packaging.python.org/guides/distributing-packages-using-setuptools/

AUTHOR = "crownet development team"
EMAIL = "stefan_schuhbaeck@hm.edu"

long_description = "omnetinireader is a Python package that reads omnetpp .ini files."

path_to_pkg_requirements = os.path.join(
    Path(__file__).absolute().parent, "requirements.txt"
)

with open(path_to_pkg_requirements, "r") as f:
    install_requires = f.readlines()
install_requires = [req.replace("\n", "") for req in install_requires]

setup(
    name="omnetinireader",
    author=AUTHOR,
    version=read_flowcontrol_version(),
    description="omnetinireader is a Python package that reads omnetpp .ini files.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    url="https://sam-dev.cs.hm.edu/rover/omnet-file-reader",
    keywords=["OMNeT++, input"],
    author_email=EMAIL,
    packages=find_packages(),
    package_dir={"omnetinireader": "omnetinireader"},
    package_data={"": ["LICENSE"]},
    python_requires=">=3.8",
    install_requires=install_requires,
    test_suite="nose.collector",
    tests_require=["nose>=1.3.7,<1.4"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
    ],
)
