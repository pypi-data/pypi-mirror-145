# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dunebuggy', 'dunebuggy.core', 'dunebuggy.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2',
 'numpy>=1.21.0,<1.22.0',
 'pandas>=1.2.4',
 'pydantic>=1.8.2',
 'sqlparse>=0.4.2']

setup_kwargs = {
    'name': 'dunebuggy',
    'version': '1.0.2',
    'description': 'A lightweight (unofficial) Python SDK for Dune.xyz',
    'long_description': None,
    'author': 'rysuds',
    'author_email': 'ryan.sudhakaran@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rysuds/dunebuggy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
