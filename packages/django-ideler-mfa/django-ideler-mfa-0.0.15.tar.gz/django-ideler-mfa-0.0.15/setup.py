#!/usr/bin/env python3
# -*- coding=utf-8 -*-

from datetime import datetime

from setuptools import find_packages
from setuptools import setup

with open("README.rst") as readme_rst:
    readme = readme_rst.read()

VERSION = 'v0.0.15'


setup(
    name="django-ideler-mfa",
    version=VERSION,
    url="https://git.ideler.de/python/django-ideler-mfa",
    author="Yannik Weiß",
    author_email="yannik.weiss@ideler.de",
    description="Multi-factor authentication for Django.",
    long_description=readme,
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "Django >= 3.0.0, < 4.0.4",
        "pyotp >= 2.6.0, <= 2.6.0",
        "segno >= 1.3.0, < 1.4.2",
    ],
    packages=find_packages(exclude=["sample"]),
)
