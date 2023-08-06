# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nba_on_court']

package_data = \
{'': ['*']}

install_requires = \
['nba-api>=1.1.8,<2.0.0', 'pandas>=1.3.5,<2.0.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'nba-on-court',
    'version': '0.1.0',
    'description': 'Adding players on court to play-by-play data',
    'long_description': None,
    'author': 'Vladislav Shufinskiy',
    'author_email': 'shufinsky.90210@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
