import requests
import numpy as np
import streamlit as st

# Symbol to id mapping (keep it for your reference)
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

# Define the API endpoint and your API key
GRAPH_URL = "https://gateway.thegraph.com/api/subgraphs/id/5zvR82QoaXYFyDEKLZ9t6v9adgnptxYpKpSbxtgVENFV"
GRAPH_API_KEY = st.secrets["THE_GRAPH_API_TOKEN"]


class MarketDataFetcher:
    def __init__(self):
        self.cache = {}  # format: { (token_id, vs_currency): token_data }

    def get_token_data(self, token_id='ethereum', vs_currency='usd'):
        token_id = SYMBOL_TO_ID.get(token_id.lower(), token_id.lower())
        cache_key = (token_id, vs_currency)

        if cache_key in self.cache:
            return self.cache[cache_key]  # ✅ use cached result

        try:
            # Construct the query based on the token_id
            query = self.construct_query(token_id)

            # API Request headers
            headers = {
                "Authorization": f"Bearer {GRAPH_API_KEY}"
            }

            # Request to The Graph API
            response = requests.post(GRAPH_URL, json={'query': query}, headers=headers)

            if response.status_code != 200:
                raise Exception(
                    f"Graph API request failed with status code {response.status_code}. Response: {response.text}")

            data = response.json()
            if 'data' not in data or 'swaps' not in data['data']:
                print("Response:", data)
                raise Exception("No swaps data found in the response.")

            swaps = data['data']['swaps']

            # Calculate price and volatility based on swap data
            price, volatility = self.calculate_price_and_volatility(swaps)

            result = {
                'token': token_id,
                'price': price,
                'volatility': volatility,
                'raw_data': swaps  # Store the raw swap data for reference
            }

            self.cache[cache_key] = result  # ✅ store in cache
            return result

        except Exception as e:
            print(f"[ERROR] Fetching market data failed: {e}")
            return None

    def construct_query(self, token_id):
        """
        Construct a GraphQL query to fetch swap data for the given token pair.
        """
        # Update this based on token pairing (BTC/ETH or other pairs)
        query = f"""
        {{
          swaps(first: 1000, orderBy: timestamp, orderDirection: desc, where: {{
            token0: "{token_id}"
          }}) {{
            timestamp
            amount0In
            amount0Out
            amount1In
            amount1Out
          }}
        }}
        """
        return query

    def calculate_price_and_volatility(self, swap_data):
        """
        Calculate the price and volatility based on swap data.
        """
        prices = []
        for swap in swap_data:
            amount0_in = float(swap['amount0In'])
            amount0_out = float(swap['amount0Out'])
            amount1_in = float(swap['amount1In'])
            amount1_out = float(swap['amount1Out'])

            # Calculate price based on swap amounts
            if amount1_in > 0:
                price = amount0_in / amount1_out  # ETH/BTC price
            elif amount1_out > 0:
                price = amount0_out / amount1_in  # BTC/ETH price
            else:
                price = 0  # Invalid swap, skip

            prices.append(price)

        # Calculate volatility based on price changes
        volatility = self.calculate_volatility(prices)
        # Return the latest price (can also return an average or a range)
        latest_price = prices[-1] if prices else None

        return latest_price, volatility

    def calculate_volatility(self, price_data):
        """
        Calculate volatility as the standard deviation of price returns.
        """
        try:
            returns = np.diff(price_data) / price_data[:-1]  # percentage changes
            volatility = np.std(returns) * 100  # in %
            return round(volatility, 4)
        except Exception as e:
            print(f"[ERROR] Calculating volatility: {e}")
            return None
