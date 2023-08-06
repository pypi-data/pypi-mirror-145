import os
from setuptools import setup

setup(
    name = "deltares_cosmos",
    version = "0.0.10",
    author = "Maarten van Ormondt",
    author_email = "maarten.vanormondt@deltares.nl",
    description = ("Deltares CoSMoS package"),
    license = "MIT",
    keywords = "cosmos",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['cosmos'],
    package_dir={'cosmos': 'src/cosmos'},
    long_description='none',
)
