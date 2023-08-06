# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scitokens', 'scitokens.jupyter']

package_data = \
{'': ['*']}

install_requires = \
['baydemir==0.0.1',
 'jupyterhub>=1.3,<1.4',
 'requests-oauthlib>=1.3,<1.4',
 'tornado>=6.1,<6.2']

setup_kwargs = {
    'name': 'scitokens-jupyter',
    'version': '0.0.3',
    'description': 'Support for SciTokens for Project Jupyter',
    'long_description': None,
    'author': 'Brian Aydemir',
    'author_email': 'baydemir@morgridge.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/scitokens/scitokens-jupyter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
