# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exrates']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0', 'requests>=2.27.1,<3.0.0']

entry_points = \
{'console_scripts': ['exrates = exrates.__main__:main']}

setup_kwargs = {
    'name': 'exrates',
    'version': '1.0.7',
    'description': 'Exrates is a simple Python application to get exchange rates',
    'long_description': None,
    'author': 'Ömer Gök',
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
