# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['internxt_data_test']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=2.34.2,<3.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pyarrow>=7.0.0,<8.0.0',
 'stripe>=2.68.0,<3.0.0']

setup_kwargs = {
    'name': 'internxt-data-test',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Joan Mora',
    'author_email': 'elcorreudejoanmora@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
