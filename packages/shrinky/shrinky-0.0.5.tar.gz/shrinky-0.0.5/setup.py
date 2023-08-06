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
    'version': '0.0.5',
    'description': 'Shrinks images in the way I want',
    'long_description': "# shrinky\n\n[![PyPI](https://img.shields.io/pypi/v/shrinky.svg)](https://pypi.org/project/shrinky/)\n\nShrinks images in the way I want\n\n## Installation\n\nInstall this library using `pip`:\n\n    $ python -m pip install shrinky\n\n## Usage\n\nIt's a CLI program, run `shrinky [OPTIONS] FILENAME`\n\n    Options:\n    -o, --output FILE\n    -t, --output-type TEXT  New file type (eg jpg, png etc.)\n    -g, --geometry TEXT     Geometry, 1x1, 1x, x1 etc.\n    -q, --quality INTEGER   If JPEG, set quality.\n    -f, --force             Overwrite destination\n    -d, --debug             Enable debug logging\n    --help                  Show this message and exit.\n\nFor example, if you want to turn `example.png` to a JPEG file at quality 45, shrunk within an 800x800 bounding box, you can go:\n\n`shrinky -t jpg -q 45 -g 800x00 example.png`\n\nYou'll end up with `example.jpg`.\n\n## Development\n\nTo contribute to this library, first checkout the code. Then create a new virtual environment:\n\n    cd shrinky\n    poetry install\n    poetry run python -m shrinky etc etc\n",
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
