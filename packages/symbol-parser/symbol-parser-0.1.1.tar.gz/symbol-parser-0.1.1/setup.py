# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['symbol_parser']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.8.0,<5.0.0', 'ready-logger>=0.1.1,<0.2.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'symbol-parser',
    'version': '0.1.1',
    'description': 'Utility class for parsing a ticker symbol and converting symbol syntax to different standards.',
    'long_description': None,
    'author': 'Dan Kelleher',
    'author_email': 'kelleherjdan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
