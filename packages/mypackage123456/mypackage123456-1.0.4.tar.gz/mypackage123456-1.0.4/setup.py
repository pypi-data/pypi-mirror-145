from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '1.0.4'
DESCRIPTION = 'Test publishing package'

test_requirements = ["pytest>=3.8"]

# Setting up
setup(
    name="mypackage123456",
    version=VERSION,
    author="Khai Truong",
    author_email="<khaitruong209@gmail.com>",
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    packages=find_packages(include=["mypackage123456"]),
    install_requires=['flask'],
    test_suite="tests",
    tests_require=test_requirements,
)
