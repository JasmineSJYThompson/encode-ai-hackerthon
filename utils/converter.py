import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt

class DeFiConverter:
    """
    A class that provides functionalities for converting between fiat and crypto in real time,
    fetching historical conversion rate data, and plotting historical data.
    """
    # Map symbols to CoinGecko IDs for major cryptocurrencies.
    CRYPTO_IDS = {
        "btc": "bitcoin",
        "eth": "ethereum",
        "doge": "dogecoin",
        "bnb": "binancecoin",
        "ada": "cardano"
    }
    
    # Define fiat currencies.
    FIAT_CURRENCIES = {"usd", "eur", "gbp", "jpy", "aud", "cad"}
    
    # Use a common reference fiat currency for ratio conversions when comparing two cryptos.
    COMMON_FIAT = "usd"
    
    # API endpoints.
    COINGECKO_SIMPLE_PRICE = "https://api.coingecko.com/api/v3/simple/price"
    COINGECKO_MARKET_CHART = "https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    
    def __init__(self):
        pass

    # ------------------- Utility Methods -------------------
    @classmethod
    def is_crypto(cls, currency: str) -> bool:
        """Return True if the currency represents a cryptocurrency."""
        return currency.lower() in cls.CRYPTO_IDS

    @classmethod
    def is_fiat(cls, currency: str) -> bool:
        """Return True if the currency represents a fiat currency."""
        return currency.lower() in cls.FIAT_CURRENCIES

    def get_crypto_price(self, coin: str, vs_currency: str = "usd") -> float:
        """
        Get the current price of a crypto coin in the specified vs_currency.

        Args:
            coin (str): crypto symbol (e.g., 'btc').
            vs_currency (str): a fiat currency (e.g., 'usd').

        Returns:
            float: Current price.
        """
        coin = coin.lower()
        vs_currency = vs_currency.lower()
        coin_id = self.CRYPTO_IDS.get(coin)
        if coin_id is None:
            raise ValueError(f"Unsupported crypto: {coin}")
        params = {
            "ids": coin_id,
            "vs_currencies": vs_currency
        }
        response = requests.get(self.COINGECKO_SIMPLE_PRICE, params=params)
        data = response.json()
        try:
            return data[coin_id][vs_currency]
        except KeyError:
            raise Exception(f"Could not retrieve price for {coin} in {vs_currency}")

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert a given amount between currencies.
        Supports fiat-to-crypto, crypto-to-fiat, and crypto-to-crypto conversions.

        Args:
            amount (float): Amount in the source currency.
            from_currency (str): The source currency symbol.
            to_currency (str): The target currency symbol.

        Returns:
            float: Converted amount.
        """
        from_currency = from_currency.lower()
        to_currency = to_currency.lower()

        print(f"[DEBUG] Converting {amount} from {from_currency} to {to_currency}.")

        # Case 1: Fiat → Crypto
        if self.is_fiat(from_currency) and self.is_crypto(to_currency):
            print("[DEBUG] Using fiat-to-crypto conversion branch.")
            price = self.get_crypto_price(to_currency, vs_currency=from_currency)
            return amount / price

        # Case 2: Crypto → Fiat
        elif self.is_crypto(from_currency) and self.is_fiat(to_currency):
            print("[DEBUG] Using crypto-to-fiat conversion branch.")
            price = self.get_crypto_price(from_currency, vs_currency=to_currency)
            return amount * price

        # Case 3: Crypto → Crypto (via a common fiat)
        elif self.is_crypto(from_currency) and self.is_crypto(to_currency):
            print("[DEBUG] Using crypto-to-crypto conversion branch.")
            price_from = self.get_crypto_price(from_currency, vs_currency=self.COMMON_FIAT)
            price_to = self.get_crypto_price(to_currency, vs_currency=self.COMMON_FIAT)
            rate = price_from / price_to
            return amount * rate

        else:
            raise ValueError("Conversion between the provided currencies is not supported (fiat-to-fiat is excluded).")

    # ------------------- Historical Data (Optional) -------------------
    def get_conversion_rate_history(self, from_currency: str, to_currency: str, days: int = 1) -> pd.DataFrame:
        """
        Fetch historical conversion rate data over the past `days`.

        For crypto-to-fiat, it fetches the coin's price history.
        For fiat-to-crypto, it inverts the coin's price history.
        For crypto-to-crypto, it fetches both coins' histories and computes their ratio.

        Args:
            from_currency (str): The source currency symbol.
            to_currency (str): The target currency symbol.
            days (int): Number of days to fetch (default is 1).

        Returns:
            pd.DataFrame: Historical data with columns "timestamp" and "conversion_rate".
        """
        from_currency = from_currency.lower()
        to_currency = to_currency.lower()

        timestamps = []
        conversion_rates = []
        prices = []

        # Crypto-to-Fiat
        if self.is_crypto(from_currency) and self.is_fiat(to_currency):
            coin_id = self.CRYPTO_IDS.get(from_currency, from_currency)
            params = {"vs_currency": to_currency, "days": days}
            url = self.COINGECKO_MARKET_CHART.format(coin_id=coin_id)
            response = requests.get(url, params=params)
            data = response.json()
            prices = data.get("prices", [])
            for ts, price in prices:
                timestamps.append(datetime.datetime.fromtimestamp(ts / 1000))
                conversion_rates.append(price)

        # Fiat-to-Crypto
        elif self.is_fiat(from_currency) and self.is_crypto(to_currency):
            coin_id = self.CRYPTO_IDS.get(to_currency, to_currency)
            params = {"vs_currency": from_currency, "days": days}
            url = self.COINGECKO_MARKET_CHART.format(coin_id=coin_id)
            response = requests.get(url, params=params)
            data = response.json()
            prices = data.get("prices", [])
            for ts, price in prices:
                timestamps.append(datetime.datetime.fromtimestamp(ts / 1000))
                # Invert the price: how many coins per 1 unit of fiat.
                conversion_rates.append(1 / price if price != 0 else 0)

        # Crypto-to-Crypto (via a common fiat)
        elif self.is_crypto(from_currency) and self.is_crypto(to_currency):
            coin_id_from = self.CRYPTO_IDS.get(from_currency, from_currency)
            coin_id_to = self.CRYPTO_IDS.get(to_currency, to_currency)
            params = {"vs_currency": self.COMMON_FIAT, "days": days}
            url_from = self.COINGECKO_MARKET_CHART.format(coin_id=coin_id_from)
            url_to = self.COINGECKO_MARKET_CHART.format(coin_id=coin_id_to)
            response_from = requests.get(url_from, params=params)
            response_to = requests.get(url_to, params=params)
            data_from = response_from.json()
            data_to = response_to.json()
            prices_from = data_from.get("prices", [])
            prices_to = data_to.get("prices", [])
            count = min(len(prices_from), len(prices_to))
            for i in range(count):
                ts = prices_from[i][0]
                price_from = prices_from[i][1]
                price_to = prices_to[i][1]
                timestamps.append(datetime.datetime.fromtimestamp(ts / 1000))
                conversion_rates.append(price_from / price_to if price_to != 0 else 0)
        else:
            raise ValueError("Historical data for fiat-to-fiat is not supported.")

        df = pd.DataFrame({
            "timestamp": timestamps,
            "conversion_rate": conversion_rates
        })
        df = df.sort_values("timestamp").reset_index(drop=True)
        return df

    def plot_history(self, from_currency: str, to_currency: str, days: int = 1):
        """
        Plot historical conversion rate data.

        Args:
            from_currency (str): The source currency symbol.
            to_currency (str): The target currency symbol.
            days (int): Number of days to plot (default is 1).
        """
        try:
            df_history = self.get_conversion_rate_history(from_currency, to_currency, days)
            plt.figure(figsize=(10, 5))
            plt.plot(df_history["timestamp"], df_history["conversion_rate"], label="Conversion Rate")
            plt.xlabel("Time")
            plt.ylabel("Conversion Rate")
            plt.title(f"Historical Conversion Rate: {from_currency.upper()} to {to_currency.upper()}")
            plt.legend()
            plt.show()
        except Exception as e:
            print("Error plotting historical data:", e)
