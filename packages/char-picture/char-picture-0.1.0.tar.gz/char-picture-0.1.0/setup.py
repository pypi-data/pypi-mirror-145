# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['char_picture']

package_data = \
{'': ['*']}

install_requires = \
['cowpy>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'char-picture',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'winfred_wu',
    'author_email': '869286203@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
