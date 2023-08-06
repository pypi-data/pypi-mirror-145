# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shazamctl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shazamctl',
    'version': '0.0.0a0',
    'description': 'Open-source Shazam CLI',
    'long_description': '# shazamctl\n\n**shazamctl is not released yet. Install it from Git:**\n\n```sh\npipx install git+https://gitlab.com/notpushkin/shazamctl\n```\n\n## Usage\n\n```\n$ shazamctl recognize path/to/rickroll.mp3\nAt 0:00:10: Never Gonna Give You Up by Rick Astley\n```\n\n```\n$ shazamctl recognize path/to/1h_hardbass_mix.mp3 --multiple\nAt 0:00:16: Russian Vodka by XS Project\nAt 0:03:21: ...\n```\n\n```\n$ shazamctl listen\nNot implemented... yet\n```\n',
    'author': 'Alexander Pushkov',
    'author_email': 'alexander@notpushk.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
