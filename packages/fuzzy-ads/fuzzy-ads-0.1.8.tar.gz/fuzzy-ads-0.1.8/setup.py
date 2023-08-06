# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fuzzy_ads']

package_data = \
{'': ['*']}

install_requires = \
['ads>=0.12.3,<0.13.0',
 'click>=8.0.4,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11.2.0,<12.0.0']

entry_points = \
{'console_scripts': ['ads = fuzzy_ads.cli:cli']}

setup_kwargs = {
    'name': 'fuzzy-ads',
    'version': '0.1.8',
    'description': 'Unofficial Command Line Interface the SAO/NASA Astrophysics Data System',
    'long_description': None,
    'author': 'Max Mahlke',
    'author_email': 'max.mahlke@oca.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxmahlke/fuzzy-ads',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
