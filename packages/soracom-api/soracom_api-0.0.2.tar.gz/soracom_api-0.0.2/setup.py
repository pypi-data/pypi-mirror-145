# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['soracom_api',
 'soracom_api.api',
 'soracom_api.apis',
 'soracom_api.model',
 'soracom_api.models']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0', 'urllib3>=1.26.9,<2.0.0']

setup_kwargs = {
    'name': 'soracom-api',
    'version': '0.0.2',
    'description': 'SORACOM API Client for the Python programming language based on the OpenAPI specification',
    'long_description': None,
    'author': 'ks6088ts',
    'author_email': 'ks6088ts@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
