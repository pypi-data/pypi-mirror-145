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
    'version': '0.5.0',
    'description': 'File Binary is a package with some tools to help you with binary files',
    'long_description': '<div align="center">\n  <h1>File Binary</h1>\n</div>\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/pandas.svg)](https://pypi.org/project/file-binary)\n\n---\n### What is it ?\n\n**File Binary** is a package with some tools to help you with binary files\n\n### How to install\n```py\npip install file-binary\n```\n### How to use\n\n```py\nfrom binary_file import fb\n```',
    'author': 'matheus',
    'author_email': 'geof.matheus@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MatheusRamo/file_binary',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
