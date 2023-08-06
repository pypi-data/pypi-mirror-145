# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['thirdweb',
 'thirdweb.abi',
 'thirdweb.abi.erc165',
 'thirdweb.abi.ierc1155',
 'thirdweb.abi.ierc20',
 'thirdweb.abi.ierc721',
 'thirdweb.abi.marketplace',
 'thirdweb.abi.t_w_factory',
 'thirdweb.abi.t_w_registry',
 'thirdweb.abi.token_erc1155',
 'thirdweb.abi.token_erc20',
 'thirdweb.abi.token_erc721',
 'thirdweb.common',
 'thirdweb.constants',
 'thirdweb.contracts',
 'thirdweb.core',
 'thirdweb.core.classes',
 'thirdweb.core.helpers',
 'thirdweb.types',
 'thirdweb.types.settings']

package_data = \
{'': ['*']}

install_requires = \
['dacite>=1.6.0,<2.0.0',
 'mypy-extensions>=0.4.3,<0.5.0',
 'thirdweb-contract-wrappers>=2.0.4,<3.0.0',
 'web3==5.27.0']

setup_kwargs = {
    'name': 'thirdweb-sdk',
    'version': '2.0.0a8',
    'description': '',
    'long_description': '# Thirdweb Python SDK\n\nThe thirdweb SDK for Python. Currently supports Mainnet, Rinkeby, Goerli, Polygon, and Mumbai.\n## Installation\n\n```bash\n$ pip install thirdweb-sdk==2.0.0a7\n```\n\n## Getting Started\n\nTo start using this SDK, you need to pass in a provider configuration, and optionally a signer if you want to send transactions.\n\n### Instantiating the SDK\n\nOnce you have all the necessary dependencies, you can follow the following setup steps to get started with the SDK (if you want to use your private key as displayed below, make sure to run `pip install python-dotenv` as well):\n\n```python\nfrom thirdweb import ThirdwebSDK\nfrom eth_account import Account\nfrom dotenv import load_dotenv\nfrom web3 import Web3\nimport os\n\n# Load environment variables into this file\nload_dotenv()\n\n# This PRIVATE KEY is coming from your environment variables. Make sure to never put it in a tracked file or share it with anyone.\nPRIVATE_KEY = os.environ.get("PRIVATE_KEY")\n\n# Add your own RPC URL here or use a public one\nRPC_URL = "https://rpc-mumbai.maticvigil.com"\n\n# Instantiate a new provider to pass into the SDK\nprovider = Web3(Web3.HTTPProvider(RPC_URL))\n\n# Optionally, instantiate a new signer to pass into the SDK\nsigner = Account.from_key(PRIVATE_KEY)\n\n# Finally, you can create a new instance of the SDK to use\nsdk = ThirdwebSDK(provider, signer)\n```\n\nIf you wanted to use the SDK with a signer above, make sure to include your PRIVATE_KEY in your `.env` file, and make sure this file is NOT tracked in any repository (make sure to add it to your `.gitignore` file). Adding your private key to your `.env` would look like the following:\n\n```\nPRIVATE_KEY=your-private-key-here\n```\n\n### Working With Contracts\n\nOnce you instantiate the SDK, you can use it to access your thirdweb contracts. You can use the SDK\'s contract getter functions like `get_token`, `get_edition`, and `get_nft_collection` to get the respective SDK contract instances. To use an NFT Collection contract for example, you can do the following.\n\n```python\n# Add this import at the top of your file\nfrom thirdweb.types.nft import NFTMetadataInput\n\n# Add your NFT Collection contract address here\nNFT_COLLECTION_ADDRESS = "0x.."\n\n# And you can instantiate your contract with just one line\nnft_collection = sdk.get_nft_collection(NFT_COLLECTION_ADDRESS)\n\n# Now you can use any of the SDK contract functions\nbalance = nft_collection.balance()\nnft_collection.mint(NFTMetadataInput.from_json({ "name": "Cool NFT", "description": "Minted with the Python SDK!" }))\n```\n\n## Development Environment\n\nIn this section, we\'ll go over the steps to get started with running the Python SDK repository locally and contributing to the code. If you aren\'t interested in contributing to the thirdweb Python SDK, you can ignore this section.\n\n### Poetry Environment Setup\n\nIf you want to work with this repository, make sure to setup [Poetry](https://python-poetry.org/docs/), you\'re virtual environment, and the code styling tools.\n\nAssuming you\'ve installed and setup poetry, you can setup this repository with:\n\n```bash\n$ poetry shell\n$ poetry install\n$ poetry run yarn global add ganache\n```\n\nAlternatively, if your system can run .sh files, you can set everything up by running the following bash script:\n\n```bash\n$ bash scripts/env/setup.sh\n```\n\n### Running Tests\n\nBefore running tests, make sure you\'ve already run `poetry shell` and are in the poetry virutal environment with all dependencies installed. \n\nOnce you have checked that this you have all the dependencies, you can run the following:\n\n```bash\n$ poetry run brownie test\n```\n\nCurrently (only temporary), since contract deployers are not yet setup in this SDK, the testing relies on contracts on testnets deployed through the thirdweb dashboard. The testing setup is configured to use the `mumbai` network currently, but this can be changed to any network by chaing the RPC URL used in `tests/fixtures/before.py`.\n\nTo properly setup testing, you\'ll need to add your private key to the `.env` file as follows:\n\n```.env\nPRIVATE_KEY=...\n```\n\nAnd then switch the test cases to use your own contract addresses for the `NFT_COLLECTION_ADDRESS`, `EDITION_ADDRESS`, and `TOKEN_ADDRESS` variables in `tests/test_nft_collection.py`, `tests/test_edition.py`, and `tests/test_token.py` files respectively.\n\n### Code Style Setup\n\nMake sure you have `mypy`, `pylint`, and `black` installed (all included in the dev dependencies with `poetry install`.\n\nIf you\'re working in VSCode, there a few steps to get everything working with the poetry .venv:\n\n1. To setup poetry virtual environment inside your VSCode so it gets recognized as part of your project (import for linters), you can take the following steps from this [stack overflow answer](https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option). You need to run `poetry config virtualenvs.in-project true` and then make sure you delete/create a new poetry env.\n2. In `.vscode/settings.json`, you should have the following:\n```json\n{\n  "python.linting.mypyEnabled": true,\n  "python.linting.enabled": true,\n  "python.linting.pylintEnabled": false\n}\n```\n3. Make sure to set your VSCode `Python: Interpreter` setting to the Python version inside your poetry virtual environment.\n\n\n### Generate Python ABI Wrappers\n\nUse the [abi-gen](https://www.npmjs.com/package/@0x/abi-gen) package to create the Python ABIs. You can install it with the following command:\n\n```bash\n$ npm install -g @0x/abi-gen\n```\n\nAssuming you have the thirdweb contract ABIs in this directory at `/abi`, you can run the following command to generate an ABI.\n\n```bash\n$ abi-gen --language Python -o thirdweb/abi --abis abi/TokenERC721.json\n```\n\nAlternatively, if your system can run .sh files, you can run the following to generate all ABIs at once (from your /abi folder):\n\n```bash\n$ bash scripts/abi/generate.sh\n```\n',
    'author': 'thirdweb',
    'author_email': 'sdk@thirdweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.7.1,<=3.10.4',
}


setup(**setup_kwargs)
