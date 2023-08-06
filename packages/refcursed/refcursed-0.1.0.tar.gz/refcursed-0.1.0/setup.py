"""Setup script for refcursed"""

# Standard library imports
import pathlib

# Third party imports
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="refcursed",
    version="0.1.0",
    description="A library for cursed refcount-based utilities",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Kylebrown9/refcursed",
    author="Kyle Brown",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["refcursed"],
)
