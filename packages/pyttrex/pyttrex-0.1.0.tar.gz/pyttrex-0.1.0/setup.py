# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyttrex']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'pyttrex',
    'version': '0.1.0',
    'description': 'Bittrex python library',
    'long_description': None,
    'author': 'Hakan Dilek',
    'author_email': 'hakandilek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
