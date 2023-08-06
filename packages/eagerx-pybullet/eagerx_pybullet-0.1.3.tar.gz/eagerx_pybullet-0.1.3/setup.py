# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eagerx_pybullet']

package_data = \
{'': ['*']}

install_requires = \
['eagerx>=0.1.12,<0.2.0', 'pybullet>=3.2.1,<4.0.0']

setup_kwargs = {
    'name': 'eagerx-pybullet',
    'version': '0.1.3',
    'description': 'This repository contains the eagerx_pybllet package, which allows to simulate systems with EAGERx using pybullet.',
    'long_description': None,
    'author': 'Bas van der Heijden',
    'author_email': 'd.s.vanderheijden@tudelft.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eager-dev/eagerx',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
