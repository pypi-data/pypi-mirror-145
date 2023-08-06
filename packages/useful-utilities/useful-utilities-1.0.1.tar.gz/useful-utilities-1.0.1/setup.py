# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['useful_utilities']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'useful-utilities',
    'version': '1.0.1',
    'description': "Various useful utilities that I created when I didn't find an alternative.",
    'long_description': None,
    'author': 'lzrdblzzrd',
    'author_email': 'lzrdblzzrd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lzrdblzzrd/useful-utilities',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
