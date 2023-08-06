# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bettermonitoring']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'bettermonitoring',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Roman',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
