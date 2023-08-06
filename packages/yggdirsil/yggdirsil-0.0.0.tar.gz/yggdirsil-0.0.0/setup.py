# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yggdirsil']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'yggdirsil',
    'version': '0.0.0',
    'description': 'Your cloud-based files, within reach.',
    'long_description': None,
    'author': 'Orlando Ospino Sánchez',
    'author_email': 'oroschz@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
