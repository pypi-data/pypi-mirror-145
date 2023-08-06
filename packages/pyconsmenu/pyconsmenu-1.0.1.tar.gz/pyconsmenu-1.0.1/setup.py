# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyconsmenu']
setup_kwargs = {
    'name': 'pyconsmenu',
    'version': '1.0.1',
    'description': 'Create menu in terminal, guide = youtube.com/watch?v=haSVq3-v1Jk',
    'long_description': None,
    'author': 'LON112',
    'author_email': 'blonylow@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
