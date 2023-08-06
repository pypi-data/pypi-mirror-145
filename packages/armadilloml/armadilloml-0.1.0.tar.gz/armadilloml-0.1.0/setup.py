# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['armadilloml']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich-click>=1.2.1,<2.0.0',
 'rich>=12.0.1,<13.0.0']

entry_points = \
{'console_scripts': ['armadilloml = armadilloml:cli']}

setup_kwargs = {
    'name': 'armadilloml',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Max Davish',
    'author_email': 'mdavish@yext.com',
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
