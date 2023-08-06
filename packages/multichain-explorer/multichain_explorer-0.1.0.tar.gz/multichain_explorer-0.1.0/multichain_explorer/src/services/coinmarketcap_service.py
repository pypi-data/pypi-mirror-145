import config
from src.services.fetch_service import FetchService

class CoinMarketCapService():
    """
    This class is used to fetch data from the CoinMarketCap API 
    """
    currency : str
    fetchService : FetchService

    def __init__(self):
        self.currency = "USD"
        self.fetchService : FetchService()

    def fetchData(self, symbol: str):
        """
        Fetch data from the CoinMarketCap API

        Args:
            symbol: the symbol of the cryptocurrency

        Returns:
            The data as a dict
        """
        try:
            params = self.get_params(symbol)
            headers = self.get_headers()

            #TODO - Use class member service
            data = FetchService().fetchJson(
                                        config.COINMARKETCAP_URL,
                                        params,
                                        headers
                                    )
            return data
        except Exception as e:
            print(e)
            raise


    def get_params(self, symbol: str):
        parameters = {
            'symbol': symbol,
            'convert': self.currency
        }
        return parameters

    def get_headers(self):
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.COINMARKETCAP_API_KEY
        }
        return headers

