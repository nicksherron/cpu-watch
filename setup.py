#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

NAME = 'cpu-watch'
DESCRIPTION = 'cpu percentage monitoring for processes'
LONG = "monitors processes to see if they are above a certain cpu percentage "\
       "for a given period of time, and if so " \
       "executes a shell command "
URL = 'https://github.com/nicksherron/cpu-watch'
EMAIL = 'nsherron90@gmail.com'
AUTHOR = 'Nick Sherron'
REQUIRES_PYTHON = '>=3.5.0'
VERSION = '0.1.0'


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    install_requires=[
        'psutil'
    ],
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
