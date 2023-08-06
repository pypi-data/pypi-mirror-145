# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dash_extensions']

package_data = \
{'': ['*']}

install_requires = \
['Flask-Caching>=1.10.1,<2.0.0',
 'dash>=2.3.0,<3.0.0',
 'jsbeautifier>=1.14.0,<2.0.0',
 'more-itertools>=8.12.0,<9.0.0']

setup_kwargs = {
    'name': 'dash-extensions',
    'version': '0.1.0rc5',
    'description': 'Extensions for Plotly Dash.',
    'long_description': None,
    'author': 'emher',
    'author_email': 'emil.h.eriksen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
