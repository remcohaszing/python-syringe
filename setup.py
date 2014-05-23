#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup

try:
    from unittest import mock
except:
    kwargs = {
        'tests_require': 'mock',
        'extras_require': {
            'mock': 'mock'
        }
    }
else:
    kwargs = {}


with open('README.rst') as f:
    readme = f.read()


setup(
    name='syringe',
    version='0.1.1',
    author='Remco Haszing',
    author_email='remcohaszing@gmail.com',
    url='https://github.com/remcohaszing/python-syringe',
    license='MIT',
    description='A simple dependency injection library',
    long_description=readme,
    py_modules=['syringe'],
    test_suite='tests',
    zip_safe=True,
    **kwargs)
