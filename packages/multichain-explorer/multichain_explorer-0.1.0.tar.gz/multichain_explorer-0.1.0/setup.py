# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multichain_explorer',
 'multichain_explorer.src',
 'multichain_explorer.src.models',
 'multichain_explorer.src.models.provider',
 'multichain_explorer.src.providers',
 'multichain_explorer.src.providers.eth',
 'multichain_explorer.src.services',
 'multichain_explorer.src.validators',
 'multichain_explorer.src.validators.eth',
 'multichain_explorer.tests.providers.eth']

package_data = \
{'': ['*'],
 'multichain_explorer': ['.git/*',
                         '.git/hooks/*',
                         '.git/info/*',
                         '.git/logs/*',
                         '.git/logs/refs/heads/*',
                         '.git/logs/refs/remotes/multichain-explorer/*',
                         '.git/objects/13/*',
                         '.git/objects/14/*',
                         '.git/objects/15/*',
                         '.git/objects/18/*',
                         '.git/objects/22/*',
                         '.git/objects/23/*',
                         '.git/objects/27/*',
                         '.git/objects/2c/*',
                         '.git/objects/2f/*',
                         '.git/objects/30/*',
                         '.git/objects/31/*',
                         '.git/objects/60/*',
                         '.git/objects/6d/*',
                         '.git/objects/6f/*',
                         '.git/objects/8a/*',
                         '.git/objects/8f/*',
                         '.git/objects/97/*',
                         '.git/objects/9a/*',
                         '.git/objects/9d/*',
                         '.git/objects/9f/*',
                         '.git/objects/a3/*',
                         '.git/objects/ae/*',
                         '.git/objects/b1/*',
                         '.git/objects/c9/*',
                         '.git/objects/cb/*',
                         '.git/objects/d5/*',
                         '.git/objects/d8/*',
                         '.git/objects/e6/*',
                         '.git/objects/ed/*',
                         '.git/objects/f0/*',
                         '.git/objects/f2/*',
                         '.git/objects/f5/*',
                         '.git/objects/f7/*',
                         '.git/refs/heads/*',
                         '.git/refs/remotes/multichain-explorer/*',
                         '.pytest_cache/*',
                         '.pytest_cache/v/cache/*']}

install_requires = \
['web3>=5.28,<6.0']

setup_kwargs = {
    'name': 'multichain-explorer',
    'version': '0.1.0',
    'description': 'A simple package to explore multiple blockchains in an homogeneous way',
    'long_description': None,
    'author': 'sdominguez894',
    'author_email': 'sdominguez894@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
