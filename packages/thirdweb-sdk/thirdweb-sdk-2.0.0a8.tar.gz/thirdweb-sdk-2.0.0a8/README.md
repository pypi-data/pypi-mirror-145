# Thirdweb Python SDK

The thirdweb SDK for Python. Currently supports Mainnet, Rinkeby, Goerli, Polygon, and Mumbai.
## Installation

```bash
$ pip install thirdweb-sdk==2.0.0a7
```

## Getting Started

To start using this SDK, you need to pass in a provider configuration, and optionally a signer if you want to send transactions.

### Instantiating the SDK

Once you have all the necessary dependencies, you can follow the following setup steps to get started with the SDK (if you want to use your private key as displayed below, make sure to run `pip install python-dotenv` as well):

```python
from thirdweb import ThirdwebSDK
from eth_account import Account
from dotenv import load_dotenv
from web3 import Web3
import os

# Load environment variables into this file
load_dotenv()

# This PRIVATE KEY is coming from your environment variables. Make sure to never put it in a tracked file or share it with anyone.
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")

# Add your own RPC URL here or use a public one
RPC_URL = "https://rpc-mumbai.maticvigil.com"

# Instantiate a new provider to pass into the SDK
provider = Web3(Web3.HTTPProvider(RPC_URL))

# Optionally, instantiate a new signer to pass into the SDK
signer = Account.from_key(PRIVATE_KEY)

# Finally, you can create a new instance of the SDK to use
sdk = ThirdwebSDK(provider, signer)
```

If you wanted to use the SDK with a signer above, make sure to include your PRIVATE_KEY in your `.env` file, and make sure this file is NOT tracked in any repository (make sure to add it to your `.gitignore` file). Adding your private key to your `.env` would look like the following:

```
PRIVATE_KEY=your-private-key-here
```

### Working With Contracts

Once you instantiate the SDK, you can use it to access your thirdweb contracts. You can use the SDK's contract getter functions like `get_token`, `get_edition`, and `get_nft_collection` to get the respective SDK contract instances. To use an NFT Collection contract for example, you can do the following.

```python
# Add this import at the top of your file
from thirdweb.types.nft import NFTMetadataInput

# Add your NFT Collection contract address here
NFT_COLLECTION_ADDRESS = "0x.."

# And you can instantiate your contract with just one line
nft_collection = sdk.get_nft_collection(NFT_COLLECTION_ADDRESS)

# Now you can use any of the SDK contract functions
balance = nft_collection.balance()
nft_collection.mint(NFTMetadataInput.from_json({ "name": "Cool NFT", "description": "Minted with the Python SDK!" }))
```

## Development Environment

In this section, we'll go over the steps to get started with running the Python SDK repository locally and contributing to the code. If you aren't interested in contributing to the thirdweb Python SDK, you can ignore this section.

### Poetry Environment Setup

If you want to work with this repository, make sure to setup [Poetry](https://python-poetry.org/docs/), you're virtual environment, and the code styling tools.

Assuming you've installed and setup poetry, you can setup this repository with:

```bash
$ poetry shell
$ poetry install
$ poetry run yarn global add ganache
```

Alternatively, if your system can run .sh files, you can set everything up by running the following bash script:

```bash
$ bash scripts/env/setup.sh
```

### Running Tests

Before running tests, make sure you've already run `poetry shell` and are in the poetry virutal environment with all dependencies installed. 

Once you have checked that this you have all the dependencies, you can run the following:

```bash
$ poetry run brownie test
```

Currently (only temporary), since contract deployers are not yet setup in this SDK, the testing relies on contracts on testnets deployed through the thirdweb dashboard. The testing setup is configured to use the `mumbai` network currently, but this can be changed to any network by chaing the RPC URL used in `tests/fixtures/before.py`.

To properly setup testing, you'll need to add your private key to the `.env` file as follows:

```.env
PRIVATE_KEY=...
```

And then switch the test cases to use your own contract addresses for the `NFT_COLLECTION_ADDRESS`, `EDITION_ADDRESS`, and `TOKEN_ADDRESS` variables in `tests/test_nft_collection.py`, `tests/test_edition.py`, and `tests/test_token.py` files respectively.

### Code Style Setup

Make sure you have `mypy`, `pylint`, and `black` installed (all included in the dev dependencies with `poetry install`.

If you're working in VSCode, there a few steps to get everything working with the poetry .venv:

1. To setup poetry virtual environment inside your VSCode so it gets recognized as part of your project (import for linters), you can take the following steps from this [stack overflow answer](https://stackoverflow.com/questions/59882884/vscode-doesnt-show-poetry-virtualenvs-in-select-interpreter-option). You need to run `poetry config virtualenvs.in-project true` and then make sure you delete/create a new poetry env.
2. In `.vscode/settings.json`, you should have the following:
```json
{
  "python.linting.mypyEnabled": true,
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false
}
```
3. Make sure to set your VSCode `Python: Interpreter` setting to the Python version inside your poetry virtual environment.


### Generate Python ABI Wrappers

Use the [abi-gen](https://www.npmjs.com/package/@0x/abi-gen) package to create the Python ABIs. You can install it with the following command:

```bash
$ npm install -g @0x/abi-gen
```

Assuming you have the thirdweb contract ABIs in this directory at `/abi`, you can run the following command to generate an ABI.

```bash
$ abi-gen --language Python -o thirdweb/abi --abis abi/TokenERC721.json
```

Alternatively, if your system can run .sh files, you can run the following to generate all ABIs at once (from your /abi folder):

```bash
$ bash scripts/abi/generate.sh
```
