# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lablift_client']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'lablift-client',
    'version': '0.1.0',
    'description': 'Access LabLift services using Python',
    'long_description': None,
    'author': 'Rafael Bizao',
    'author_email': 'rabizao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
