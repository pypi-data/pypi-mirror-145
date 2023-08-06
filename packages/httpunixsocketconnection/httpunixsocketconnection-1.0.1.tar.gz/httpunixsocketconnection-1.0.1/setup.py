# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['httpunixsocketconnection']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'httpunixsocketconnection',
    'version': '1.0.1',
    'description': 'Really small Python class that extends native http.client.HTTPConnection allowing sending HTTP requests to Unix Sockets',
    'long_description': '# HTTPUnixSocketConnection\n\nReally small Python class that extends native http.client.HTTPConnection allowing sending HTTP requests to Unix Sockets\n\n## Installation\n\n### Poetry\n\n```sh\npoetry add httpunixsocketconnection\n```\n\n### pip\n\n```sh\npip install httpunixsocketconnection\n```\n\n## Usage\n\nBecause the class base is `http.client.HTTPConnection`, the API is almost the same.\nOnly the constructor and `connect` method is different.\nWith the rest please follow [the official docs](https://docs.python.org/3.8/library/http.client.html#http.client.HTTPConnection).\n\n```python\nfrom httpunixsocketconnection import HTTPUnixSocketConnection\n\n# Create a connection\nconn = HTTPUnixSocketConnection(\n    unix_socket="/var/run/some.unix.socket"\n    # timeout=Like in HTTPConnection\n    # blocksize=Like in HTTPConnection\n)\n```\n\n### Example: Getting list of Docker Containers\n\n```python\nfrom httpunixsocketconnection import HTTPUnixSocketConnection\n\nconn = HTTPUnixSocketConnection("/var/run/docker.sock")\nconn.request("GET", "/containers/json")\n\nres = conn.getresponse()\nprint(res.status, res.reason)\n\ncontent = res.read().decode("utf-8")\nprint(content)\n```\n',
    'author': 'Marek Sierociński',
    'author_email': 'mareksierocinski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/marverix/HTTPUnixSocketConnection',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
