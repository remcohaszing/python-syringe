#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

try:
    from unittest import mock
except:
    tests_require = ['mock']
else:
    tests_require = []


with open('README.rst') as f:
    readme = f.read()


setup(
    name='syringe',
    version='0.1.0',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    url='https://github.com/remcohaszing/python-syringe',
    license='MIT',
    description='A simple dependency injection library',
    long_description=readme,
    py_modules=['syringe'],
    test_suite='tests',
    tests_require=tests_require,
    zip_safe=True)
