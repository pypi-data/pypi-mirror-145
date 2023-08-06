# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['externalpyoverlay']
setup_kwargs = {
    'name': 'externalpyoverlay',
    'version': '1.0.0',
    'description': 'Simple lib to draw graphic primitives in not fullscreen mode.',
    'long_description': None,
    'author': 'Xenely',
    'author_email': 'a.maryatkin14@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
