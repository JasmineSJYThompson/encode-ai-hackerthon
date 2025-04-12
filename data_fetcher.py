# data_fetcher.py

from pycoingecko import CoinGeckoAPI
import numpy as np

SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "usdc": "usd-coin",
    "usdt": "tether",
    "bnb": "binancecoin",
    "sol": "solana",
    "ada": "cardano",
    "matic": "polygon",
    "dot": "polkadot",
    "ltc": "litecoin",
    "gbp": "gbp",
    "usd": "usd"
    # add more as needed
}

class MarketDataFetcher:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.cache = {}  # format: { (token_id, vs_currency): token_data }

    def get_token_data(self, token_id='ethereum', vs_currency='usd'):
        token_id = SYMBOL_TO_ID.get(token_id.lower(), token_id.lower())
        cache_key = (token_id, vs_currency)

        if cache_key in self.cache:
            print("Using cached result")
            return self.cache[cache_key]  # ✅ use cached result

        try:
            print("Fetching data")
            data = self.cg.get_coin_market_chart_by_id(id=token_id, vs_currency=vs_currency, days=1)
            print("Fetching current price")
            current_price = self.cg.get_price(ids=token_id, vs_currencies=vs_currency)
            print("Fetching market data")
            market_data = self.cg.get_coin_by_id(token_id)['market_data']
            print("Fetching volatility")
            volatility = self.calculate_volatility(data['prices'])

            result = {
                'token': token_id,
                'price': current_price[token_id][vs_currency],
                'market_cap': market_data['market_cap'][vs_currency],
                '24h_volume': market_data['total_volume'][vs_currency],
                'price_change_24h': market_data['price_change_percentage_24h'],
                'volatility': volatility,
                'raw_chart_data': data['prices']  # keep only what's used
            }

            self.cache[cache_key] = result  # ✅ store in cache
            return result

        except Exception as e:
            print(f"[ERROR] Fetching market data failed: {e}")
            return None

    
    def calculate_volatility(self, price_data):
        """
        price_data: list of [timestamp, price] from CoinGecko
        Returns: volatility = standard deviation of returns
        """
        try:
            prices = [p[1] for p in price_data]
            returns = np.diff(prices) / prices[:-1]  # percentage changes
            volatility = np.std(returns) * 100  # in %
            return round(volatility, 4)
        except Exception as e:
            print(f"[ERROR] Calculating volatility: {e}")
            return None
    