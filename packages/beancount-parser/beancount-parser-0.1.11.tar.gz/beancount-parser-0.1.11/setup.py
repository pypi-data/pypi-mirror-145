# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beancount_parser']

package_data = \
{'': ['*'], 'beancount_parser': ['grammar/*']}

install_requires = \
['lark>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'beancount-parser',
    'version': '0.1.11',
    'description': 'Standalone Lark based Beancount syntax parser (not relying on Beancount library), MIT license',
    'long_description': None,
    'author': 'Fang-Pen Lin',
    'author_email': 'fangpen@launchplatform.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LaunchPlatform/beancount-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
