from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.0.3'
DESCRIPTION = 'Test publishing package'

# Setting up
setup(
    name="mypackage123456",
    version=VERSION,
    author="Khai Truong",
    author_email="<khaitruong209@gmail.com>",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(include=["mypackage"]),
    install_requires=['flask'],
)
