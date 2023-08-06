# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['scripts']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'agadoodoo',
    'version': '0.1.2',
    'description': '',
    'long_description': 'hello world from peotry',
    'author': 'daniel',
    'author_email': 'dsal3389@dsal389.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
