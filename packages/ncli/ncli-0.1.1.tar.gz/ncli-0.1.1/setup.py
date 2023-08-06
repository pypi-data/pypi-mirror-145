# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli', 'cli.commands', 'cli.core', 'cli.core.host', 'cli.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'pydantic>=1.9.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'rich>=12.0.1,<13.0.0',
 'scrapli[full]>=2022.1.30,<2023.0.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['ncli = cli.main:app']}

setup_kwargs = {
    'name': 'ncli',
    'version': '0.1.1',
    'description': '',
    'long_description': '# NCLI\n\nNetwork command line tool',
    'author': 'Ryan Bradshaw',
    'author_email': 'ryan@rbradshaw.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
