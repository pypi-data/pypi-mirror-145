# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unicode2hex']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['unicode2hex = unicode2hex.main:run']}

setup_kwargs = {
    'name': 'unicode2hex',
    'version': '0.0.1',
    'description': 'Help get utf-8 hex representation of a unicode value or character',
    'long_description': None,
    'author': 'tizee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tizee/unicode2hex',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
