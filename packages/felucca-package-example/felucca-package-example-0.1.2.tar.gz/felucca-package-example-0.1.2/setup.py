# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['felucca_package_example']

package_data = \
{'': ['*']}

install_requires = \
['cairo-nile>=0.4.0,<0.5.0',
 'ecdsa>=0.17.0,<0.18.0',
 'fastecdsa>=2.2.3,<3.0.0',
 'felucca>=0.0.10,<0.0.11',
 'starknet.py>=0.2.0-alpha.0,<0.3.0',
 'sympy>=1.10,<2.0']

setup_kwargs = {
    'name': 'felucca-package-example',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'franalgaba',
    'author_email': 'f.algaba@outlook.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.11,<3.9',
}


setup(**setup_kwargs)
