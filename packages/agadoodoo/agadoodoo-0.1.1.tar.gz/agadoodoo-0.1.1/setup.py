# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['foo']
setup_kwargs = {
    'name': 'agadoodoo',
    'version': '0.1.1',
    'description': '',
    'long_description': '',
    'author': 'daniel',
    'author_email': 'dsal3389@dsal389.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
