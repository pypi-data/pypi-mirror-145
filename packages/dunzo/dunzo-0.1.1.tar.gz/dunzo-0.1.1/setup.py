# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dunzo']

package_data = \
{'': ['*'], 'dunzo': ['sound_effects/*']}

install_requires = \
['click>=8.1.1,<9.0.0',
 'ipython>=8.1.1,<9.0.0',
 'isort>=5.10.1,<6.0.0',
 'playsound>=1.3.0,<2.0.0',
 'pyobjc>=8.4.1,<9.0.0']

entry_points = \
{'console_scripts': ['done = dunzo.cli:cli', 'format = util.format:format']}

setup_kwargs = {
    'name': 'dunzo',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
