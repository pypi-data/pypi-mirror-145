# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opensqli']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'aiolimiter>=1.0.0,<2.0.0',
 'cchardet>=2.1.7,<3.0.0']

setup_kwargs = {
    'name': 'opensqli',
    'version': '0.1.0',
    'description': 'OpenAPI SQLi Scanner',
    'long_description': None,
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/openapi-sqli-scanner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
