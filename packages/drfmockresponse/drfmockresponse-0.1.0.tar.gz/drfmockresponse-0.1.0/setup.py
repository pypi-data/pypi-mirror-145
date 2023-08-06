# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drfmockresponse', 'drfmockresponse.migrations']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.0,<5.0', 'djangorestframework>=3.13.1,<4.0.0']

setup_kwargs = {
    'name': 'drfmockresponse',
    'version': '0.1.0',
    'description': 'Library to mock responses in Django Rest Framework.',
    'long_description': None,
    'author': 'Kostas Konstantopoulos',
    'author_email': 'ntopoulos@yahoo.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
