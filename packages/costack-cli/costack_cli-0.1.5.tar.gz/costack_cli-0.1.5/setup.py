# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['costack_cli', 'costack_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['awscli>=1.22.23,<2.0.0',
 'boto3>=1.20.23,<2.0.0',
 'inquirer>=2.9.1,<3.0.0',
 'pyOpenSSL>=22.0.0,<23.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['costack = costack_cli.main:main']}

setup_kwargs = {
    'name': 'costack-cli',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'perseus.yang',
    'author_email': 'ry82@cornell.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
