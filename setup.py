#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='hub',
    version='1.0.1',
    description="AASHE's Campus Sustainability Hub",
    author="AASHE, Lincoln Loop",
    author_email='it@aashe.org, info@lincolnloop.com',
    url='',
    packages=find_packages(),
    package_data={'hub': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)
