# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httpunixsocketconnection']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'httpunixsocketconnection',
    'version': '1.0.0',
    'description': 'Really small Python class that extends native http.client.HTTPConnection allowing sending HTTP requests to Unix Sockets',
    'long_description': None,
    'author': 'Marek Sierociński',
    'author_email': 'mareksierocinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
