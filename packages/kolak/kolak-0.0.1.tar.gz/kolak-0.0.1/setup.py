#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='kolak',
    version='v0.0.1',
    packages=['kolak', ],
    license='MIT',
    author="guangrei",
    author_email="myawn@pm.me",
    description="universal rss parser with AI",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="rss feed parser podcast xml",
    url="https://github.com/guangrei/Kolak",
)
