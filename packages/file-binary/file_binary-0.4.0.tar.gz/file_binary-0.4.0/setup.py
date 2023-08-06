# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['file_binary']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.22.3,<2.0.0']

setup_kwargs = {
    'name': 'file-binary',
    'version': '0.4.0',
    'description': 'File Binary is a package with some tools to help you with binary files',
    'long_description': None,
    'author': 'matheus',
    'author_email': 'geof.matheus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
