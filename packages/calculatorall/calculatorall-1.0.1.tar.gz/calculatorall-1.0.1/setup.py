# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['calculatorall']
setup_kwargs = {
    'name': 'calculatorall',
    'version': '1.0.1',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
}


setup(**setup_kwargs)
