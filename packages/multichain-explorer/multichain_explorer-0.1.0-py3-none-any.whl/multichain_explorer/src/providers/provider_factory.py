
from src.providers.eth.provider import EthProvider
from src.providers.provider import ProviderInterface
from src.models.blockchains import Blockchains

class BlockchainProvider():

    def get_instance(blockchain_id: Blockchains) -> ProviderInterface:
        """
        Get the blockchain provider instance

        Args:
            blockchain_id: the blockchain id as an enum
        
        Returns:
            The blockchain provider instance wrapped in a ProviderInterface
        """
        match blockchain_id:
            case Blockchains.BTC:
                return None
            case Blockchains.ETH:
                return EthProvider()
            case Blockchains.ADA:
                return None
            case Blockchains.ALGO:
                return None
            case Blockchains.LUNA:
                return None