#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata LLC
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'rdconfig',
    version = '1.1.0',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    license = 'Apache License',
    author = 'hulilei',
    author_email = 'hulilei@takewiki.com.cn',
    url = 'http://www.reshapedata.com',
    description = 'read config file in py language ',
    keywords = ['reshapedata', 'cdconfig'],
    python_requires='>=3.6',
)
