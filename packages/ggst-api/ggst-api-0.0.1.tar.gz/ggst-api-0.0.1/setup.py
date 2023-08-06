# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['GGST']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.3,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'ggst-api',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'UnknownMemory',
    'author_email': 'https://github.com/UnknownMemory',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
