import pytest
from src.providers.provider import ProviderInterface
from src.providers.eth.provider import EthProvider


@pytest.fixture
def provider() -> ProviderInterface:
    """Setup a provider instance to enable the retrieval of Ethereum data"""
    return EthProvider()


@pytest.fixture
def address() -> str:
    """Return an address used to test the provider"""
    return "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F"

def test_get_address(provider: ProviderInterface, address: str):
    """Test whether the provider returns the correct address data"""
    assert provider.get_address(address)["address"] == "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F"


@pytest.fixture
def block_number() -> str:
    """Return a block number used to test the provider"""
    return "1"

def test_get_block_by_id(provider: ProviderInterface, block_number: str):
    """Test whether the provider returns the correct block data"""
    assert provider.get_block_by_id(block_number) == {
        "id": 1,
        "miner": "0x05a56E2D52c817161883f50c441c3228CFe54d9f",
        "difficulty": 17171480576,
        "timestamp": 1438269988
    }


@pytest.fixture
def tx_id() -> str:
    """Return a transaction id used to test the provider"""
    return "0x9a72dba1ff86ab68eb9e5074134b993d0eda143be6420bc73aab5c1f99b66c92"

def test_get_transaction_by_id(provider: ProviderInterface, tx_id: str):
    """Test whether the provider returns the correct transaction data"""
    assert provider.get_transaction_by_id(tx_id) == {
        "id": "0x9a72dba1ff86ab68eb9e5074134b993d0eda143be6420bc73aab5c1f99b66c92",
        "from": "0xDFd5293D8e347dFe59E90eFd55b2956a1343963d",
        "to": "0xEC471BE76460b252a9Aec4e9CE3A94933DA79616",
        "value": 67131140000000000,
        "block": 14528351
    }