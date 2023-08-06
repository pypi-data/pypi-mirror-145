# -*- coding: utf-8 -*-

import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
else:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()

setup(
    name='firstlanguage_python',
    version='2.5.1',
    description='Python client library for FirstLanguage API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='FirstLanguage',
    author_email='info@firstlanguage.in',
    url='https://www.firstlanguage.in/contactus',
    download_url = 'https://github.com/FirstLanguage/firstlanguage_python/archive/refs/tags/v2.5.tar.gz',
    keywords = ['FirstLanguage API', 'NLP', 'SDK', 'Python', 'Natural Language Processing'],  
    packages=find_packages(),
    install_requires=[
        'jsonpickle~=1.4, >= 1.4.1',
        'requests~=2.25',
        'cachecontrol~=0.12.6',
        'python-dateutil~=2.8.1',
        'jsonschema~=3.2.0'
    ],
    tests_require=[
        'nose>=1.3.7'
    ],
    test_suite = 'nose.collector'
)