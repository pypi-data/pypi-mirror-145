import os
from setuptools import setup

setup(
    name = "deltares_coastalhazardstoolkit",
    version = "0.0.7",
    author = "Maarten van Ormondt",
    author_email = "maarten.vanormondt@deltares.nl",
    description = ("Deltares Coastal Hazards Toolkit"),
    license = "MIT",
    keywords = "deltars coastal hazards toolkit",
    url = "http://packages.python.org/an_example_pypi_project",
    packages=['cht'],
    package_dir={'cht': 'src/cht'},
    long_description='none',
)
