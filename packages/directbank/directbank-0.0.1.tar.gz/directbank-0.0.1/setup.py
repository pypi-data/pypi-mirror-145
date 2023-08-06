# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['directbank']
install_requires = \
['xsdata>=22.3,<23.0']

setup_kwargs = {
    'name': 'directbank',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Toony',
    'author_email': 'kizyanov@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
