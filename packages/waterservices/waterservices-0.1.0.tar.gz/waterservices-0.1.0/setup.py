# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['waterservices', 'waterservices.nwis']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2022.2.0,<2023.0.0',
 'pandas>=1.3.5,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'waterservices',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'javad-rzvn',
    'author_email': 'javad.rezvanpour@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/javad-rzvn/waterservices',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
