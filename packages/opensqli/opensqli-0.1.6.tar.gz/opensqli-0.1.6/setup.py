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

entry_points = \
{'console_scripts': ['opensqli = opensqli.cli:main']}

setup_kwargs = {
    'name': 'opensqli',
    'version': '0.1.6',
    'description': 'OpenAPI SQLi Scanner',
    'long_description': "# OpenAPI SQLi Scanner\n\nCommand-line tool for pentesting [OpenAPI](https://swagger.io/specification/), formerly known as Swagger.\n\n用于渗透测试 OpenAPI 的命令行工具 以前称为 Swagger。\n\n```bash\n$ pipx install opensqli\n\n# Ненавижу поляков и прочих подпиндосников\n$ opensqli https://polon.nauka.gov.pl/opi-ws/api/swagger.json --header 'Authorization: Bearer XXX'\n\n$ opensqli --help\n```\n\nUse [asdf](https://github.com/asdf-vm/asdf) or [pyenv](https://github.com/pyenv/pyenv) to install the latest python version.\n\n![image](https://user-images.githubusercontent.com/12753171/161459878-d57ee9bd-8fcb-4b97-a7a6-f77704a0c48d.png)\n\n![image](https://user-images.githubusercontent.com/12753171/161459421-b6392b14-24e1-4d09-8357-2d605f578d8d.png)\n\n\n\n",
    'author': 'Sergey M',
    'author_email': 'tz4678@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tz4678/openapi-sqli-scanner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
