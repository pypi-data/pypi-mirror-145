# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['udtool']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['udtool = udtool.console:run']}

setup_kwargs = {
    'name': 'udtool',
    'version': '0.1.0',
    'description': 'A deploy tool for UnrealEngine',
    'long_description': '',
    'author': 'Marc Seiler',
    'author_email': 'mseielr@crazyfacegames.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
