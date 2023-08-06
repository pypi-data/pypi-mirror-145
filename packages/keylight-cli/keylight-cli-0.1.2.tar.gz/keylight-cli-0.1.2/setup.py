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
    'version': '0.1.2',
    'description': 'A Python based CLI to control Elgato Keylights',
    'long_description': '# keylight-cli\n\nA Python CLI module designed to control the [Elgato](https://www.elgato.com/en) brand Lights. Use this when you want a simple command line to control your keylight. Currently only tested with a Keylight Air.\n\nThis was originally created for my purposes, allowing me to control a Keylight Air using a Stream Deck under Linux (using the python [streamdeck-ui](https://pypi.org/project/streamdeck-ui/) module)\n\n## Dependencies\nThis uses the excellent [leglight](https://gitlab.com/obviate.io/pyleglight) python module, and wraps it in a very simple CLI tool.\n\n## Usage\nThe CLI supports multiple keylights on a single network. You can target a specific light with a `-s <serial number>` parameter before any command. \nIf no serial number is provided, then the CLI will use the first one found on the network (not necessarily guaranteed to be the same one each time).\nFor best results, specify the serial number if you have multiple keylights to control\n\nRun the command without any arguments to see the help\n\n### List\n\n```\n% keylight list\nFound 1 lights\nLight <SERIAL> at <IP>:<PORT>\n```\n\n### Info\n\n```\n% keylight info\nGetting information from <SERIAL>\nLight <SERIAL> at <IP>:<PORT>\nState             : ON\nBrightness        : 10 %\nColor Temperature : 4300.0 K\n```\n\n### Control\n```\n% keylight on\nTurning on <SERIAL>\n% keylight off\nTurning off <SERIAL>\n```\n\n\n### Brightness\n```\n% keylight set-brightness 50\nSetting brightness for <SERIAL> to 50%\n```\n\n### Color Temperature\n```\n% keylight set-color-temperature 5000\nSetting color temperature for <SERIAL> to 5000K\n```\n\n## License\nMIT\n\n## Copyright\nElgato, Key Light and other product names are copyright of their owner, CORSAIR. \n',
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
