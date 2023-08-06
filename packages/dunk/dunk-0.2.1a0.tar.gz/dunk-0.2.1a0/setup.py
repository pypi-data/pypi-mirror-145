# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dunk']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.1.0,<13.0.0', 'unidiff>=0.7.3,<0.8.0']

entry_points = \
{'console_scripts': ['dunk = dunk.dunk:main']}

setup_kwargs = {
    'name': 'dunk',
    'version': '0.2.1a0',
    'description': '',
    'long_description': None,
    'author': 'Darren Burns',
    'author_email': 'darrenb900@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
