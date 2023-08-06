# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['barstow']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.1,<2.0.0', 'pyarrow>=7.0.0,<8.0.0']

setup_kwargs = {
    'name': 'barstow',
    'version': '0.1.0',
    'description': 'Library for managing Arrow datasets',
    'long_description': None,
    'author': 'Mat Leonard',
    'author_email': 'leonard.mat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
