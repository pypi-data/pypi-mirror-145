# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bookapi_t_sb032622']

package_data = \
{'': ['*']}

install_requires = \
['Flask-RESTful>=0.3.9,<0.4.0', 'Flask>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'bookapi-t-sb032622',
    'version': '1.0.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
