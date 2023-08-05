# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['openweatherclass']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'openweatherclass',
    'version': '0.4.0',
    'description': 'An implementation of the Openweather API in Python.',
    'long_description': None,
    'author': 'Brian Hudson',
    'author_email': 'reallybrianhudson@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
