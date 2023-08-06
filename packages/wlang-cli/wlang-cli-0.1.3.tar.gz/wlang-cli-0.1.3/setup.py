# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wlang_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.0,<9.0.0', 'wcore-py>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'wlang-cli',
    'version': '0.1.3',
    'description': 'A cli for the W programming language',
    'long_description': None,
    'author': 'James Butcher',
    'author_email': 'jamesbutcher@duck.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
