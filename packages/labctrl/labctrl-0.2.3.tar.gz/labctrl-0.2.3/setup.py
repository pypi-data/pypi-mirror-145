# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labctrl']

package_data = \
{'': ['*']}

install_requires = \
['PySide6>=6.2.3,<7.0.0',
 'PyVISA-py>=0.5.2,<0.6.0',
 'PyVISA>=1.11.3,<2.0.0',
 'PyYAML>=6.0,<7.0',
 'Pyro5>=5.13.1,<6.0.0',
 'loguru>=0.6.0,<0.7.0',
 'numpy>=1.21.3,<2.0.0']

setup_kwargs = {
    'name': 'labctrl',
    'version': '0.2.3',
    'description': 'A unified framework for controlling programmable lab instruments',
    'long_description': None,
    'author': 'Atharv Joshi',
    'author_email': 'atharvjoshi@ymail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
