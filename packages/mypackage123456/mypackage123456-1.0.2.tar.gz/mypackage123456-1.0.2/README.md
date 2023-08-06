Steps:

- Change the package name in setup.py (name=... in setup() function) to anything you want, as long as it does not conflict with other public packages.
- pip install wheel twine
- python setup.py sdist bdist_wheel
- twine upload dist/*
- Provide username and password of PyPi account.