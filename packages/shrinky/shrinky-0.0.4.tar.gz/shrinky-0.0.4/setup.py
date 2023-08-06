# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shrinky']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.1,<10.0.0', 'click>=8.0.4,<9.0.0', 'loguru>=0.6.0,<0.7.0']

entry_points = \
{'console_scripts': ['shrinky = shrinky.__main__:cli']}

setup_kwargs = {
    'name': 'shrinky',
    'version': '0.0.4',
    'description': 'Shrinks images in the way I want',
    'long_description': None,
    'author': 'James Hogkinson',
    'author_email': 'james@terminaloutcomes.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
