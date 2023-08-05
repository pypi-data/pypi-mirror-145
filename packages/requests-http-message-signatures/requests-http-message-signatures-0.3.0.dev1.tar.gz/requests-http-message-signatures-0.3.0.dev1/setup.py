# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_http_message_signatures']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=1.8.2', 'requests>=2,<3']

setup_kwargs = {
    'name': 'requests-http-message-signatures',
    'version': '0.3.0.dev1',
    'description': '',
    'long_description': None,
    'author': 'Funkwhale Collective',
    'author_email': 'maintainers@funkwhale.audio',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
