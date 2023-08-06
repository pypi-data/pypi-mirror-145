from importlib.resources import read_text
import string
from attr import attrs
from django import setup
import setuptools
from pathlib import Path

setuptools.setup(
    name="pdftouplodhogaaaj",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])
)
