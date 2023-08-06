# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['keylight_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.2,<9.0.0', 'leglight>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['keylight = keylight_cli.keylight_cli:start']}

setup_kwargs = {
    'name': 'keylight-cli',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Ben Lyall',
    'author_email': 'ben@lyall.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benlyall/keylight-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
