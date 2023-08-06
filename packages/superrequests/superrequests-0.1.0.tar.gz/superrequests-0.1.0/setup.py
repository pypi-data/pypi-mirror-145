# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['superrequests']

package_data = \
{'': ['*']}

install_requires = \
['requests-toolbelt>=0.9.1,<0.10.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'superrequests',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Dani Hodovic',
    'author_email': 'dani.hodovic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
