# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postgresqlite']

package_data = \
{'': ['*']}

install_requires = \
['pg8000>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'postgresqlite',
    'version': '0.1.1',
    'description': 'Python package that gives you the power of a PostgreSQL server, with the convenience of the sqlite3 package.',
    'long_description': None,
    'author': 'Frank van Viegen',
    'author_email': 'pp@vanviegen.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
