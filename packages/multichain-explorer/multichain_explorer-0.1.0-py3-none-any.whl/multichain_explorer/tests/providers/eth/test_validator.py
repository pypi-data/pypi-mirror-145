import pytest
from src.validators.validator import ValidatorInterface
from src.validators.eth.validator import EthValidator


@pytest.fixture
def validator() -> ValidatorInterface:
    """Setup a validator instance for Ethereum resources"""
    return EthValidator()


@pytest.mark.parametrize("address, expected_result", [
    ("0x56Eddb7aa87536c09CCc2793473599fD21A8b17F", True),
    ("0xEF43aA45d20752aCf6D65d0AA2642D303ECf2538", True),
    ("123", False),
    ("0xEF43-A45d2_752aCf6D!5d0AA2_42D303ECf2538", False)
])
def test_is_valid_address(validator: ValidatorInterface, address: str, expected_result: bool):
    """Test whether the validator correctly identifies valid Ethereum addresses"""
    assert validator.is_address(address) == expected_result


@pytest.mark.parametrize("block_number, expected_result", [
    ("1", True),
    ("14534022", True),
    ("abc", False),
    ("123ae45", False)
])
def test_is_valid_block_number(validator: ValidatorInterface, block_number: str, expected_result: bool):
    """Tests whether the validator correctly identifies valid Ethereum block numbers"""
    assert validator.is_block(block_number) == expected_result


@pytest.mark.parametrize("tx_id, expected_result", [
    ("0x1c97dc954f0825ae93a92e0b4808b7304e1fd4d12f712e80fe247566e269e90a", True),
    ("0x0401576f273e58ac2f299c14df7f9f1955640fa439b563c283946a0593cdb993", True),
    ("123", False),
    ("0x1c97dc954f0825ae93a92e-#$_-&,:-a304e1fd4d12f712e80fe247566e269e9", False)
])
def test_is_valid_transaction_id(validator: ValidatorInterface, tx_id: str, expected_result: bool):
    """Tests whether the validator correctly identifies valid Ethereum transaction IDs"""
    assert validator.is_transaction(tx_id) == expected_result