#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

try:
    from unittest import mock  # noqa
except ImportError:
    tests_require = ['mock']
else:
    tests_require = []


with open('README.rst') as f:
    readme = f.read()


setup(
    name='syringe',
    version='0.4.0',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    url='https://github.com/remcohaszing/python-syringe',
    license='MIT',
    description='A simple dependency injection library',
    long_description=readme,
    py_modules=['syringe'],
    extras_require={
        'mock:"2" in python_version': ['mock']
    },
    tests_require = tests_require,
    test_suite='tests',
    zip_safe=True)
