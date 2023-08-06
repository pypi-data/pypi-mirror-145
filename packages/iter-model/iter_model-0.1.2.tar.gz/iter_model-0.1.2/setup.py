# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iter_model']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'iter-model',
    'version': '0.1.2',
    'description': 'Provides models for convenient and efficient iteration',
    'long_description': '# Iter Model\n\n[![Supported Versions](https://img.shields.io/badge/python-3.10%2B-blue)](https://shields.io/)\n\n## Description\n\nTODO: add description\n',
    'author': 'volodymyrb',
    'author_email': 'volodymyr.borysiuk0@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/VolodymyrBor/iter_model',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
