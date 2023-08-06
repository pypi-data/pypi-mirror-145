# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pedanlib', 'pedanlib.src.CanRisk', 'pedanlib.src.Pedigree']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pedanlib',
    'version': '1.0.0',
    'description': 'Pedigree Analysis Library',
    'long_description': None,
    'author': 'Ramin Monajemi',
    'author_email': 'r.monajemi@lumc.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
