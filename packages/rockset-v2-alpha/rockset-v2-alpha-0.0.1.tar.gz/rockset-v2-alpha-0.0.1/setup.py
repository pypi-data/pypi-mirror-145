# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rockset', 'rockset.api', 'rockset.apis', 'rockset.model', 'rockset.models']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rockset-v2-alpha',
    'version': '0.0.1',
    'description': 'The python client for the Rockset API.',
    'long_description': None,
    'author': 'Rockset',
    'author_email': 'support@rockset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
