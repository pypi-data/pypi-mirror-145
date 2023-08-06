# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['web3_multi_provider']

package_data = \
{'': ['*']}

install_requires = \
['prometheus-client==0.13.1', 'web3>=5.28.0,<6.0.0']

setup_kwargs = {
    'name': 'web3-multi-provider',
    'version': '0.1.0',
    'description': 'Web3py provider that makes it easy to switch between different blockchain nodes to make sure application will be be online if main blockchain node will be unavailable.',
    'long_description': '# <img src="https://docs.lido.fi/img/logo.svg" alt="Lido" width="46"/>\u2003Web3 Multi Provider\n\n[![codecov](https://codecov.io/gh/lidofinance/python-base-template/branch/master/graph/badge.svg)](https://codecov.io/gh/lidofinance/lido-python-sdk)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![GitHub Super-Linter](https://github.com/lidofinance/python-base-template/workflows/Lint%20Code%20Base/badge.svg)](https://github.com/marketplace/actions/super-linter)\n\nProvider that switch to other working web3 rpc endpoint if smth is bad with active one.\n\n## Install\n\n```bash\n$ pip install web3-multi-provider\n```  \nor  \n```bash\n$ pertry add web3-multi-provider\n```  \n\n## Usage\n\n```py\nfrom web3 import Web3\nfrom web3_multi_provider import MultiHTTPProvider\n\nw3 = Web3(MultiHTTPProvider([  # RPC endpoints list\n    \'https://mainnet.infura.io/v3/...\',  # RPC endpoint 2\n    \'http://127.0.0.1:8000/\',  # RPC endpoint 1\n]))\n\nlast_block = w3.eth.get_block(\'latest\')\n```\n\n## For developers\n\n1. `poetry install` - to install deps\n2. `pre-commit install` - to install pre-commit hooks\n\n## Tests\n\n```bash\npoetry run pytest tests\n```\n',
    'author': 'Raman',
    'author_email': 'roman.s@p2p.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
