# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eth_hentai', 'eth_hentai.uniswap_v2', 'eth_hentai.uniswap_v3']

package_data = \
{'': ['*'], 'eth_hentai': ['abi/*', 'abi/uniswap_v3/*']}

install_requires = \
['psutil>=5.9.0,<6.0.0', 'web3[tester]>=5.26.0,<6.0.0']

extras_require = \
{':extra == "docs"': ['sphinx-autodoc-typehints[docs]>=1.16.0,<2.0.0'],
 'docs': ['Sphinx>=4.4.0,<5.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinx-sitemap>=2.2.0,<3.0.0']}

setup_kwargs = {
    'name': 'eth-hentai',
    'version': '0.6.1',
    'description': 'Common Ethereum smart contracts, and related utilities, for developing automated test suites, backend integration and trading bots for EVM based blockchains.',
    'long_description': '[This package has been renamed to Web3 Ethereum Defi](https://github.com/tradingstrategy-ai/web3-ethereum-defi).\n\n',
    'author': 'Mikko Ohtamaa',
    'author_email': 'mikko@capitalgram.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tradingstrategy.ai',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
