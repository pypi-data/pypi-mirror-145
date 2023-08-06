# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redkernel']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'redkernel',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Stanislav',
    'author_email': 'me@h3xco.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
