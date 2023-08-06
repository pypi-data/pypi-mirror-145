# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['backlog_schema']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'backlog-schema',
    'version': '0.1.0',
    'description': 'backlog.com の pydantic model',
    'long_description': None,
    'author': 'Niten Nashiki',
    'author_email': 'n.nashiki.work@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
