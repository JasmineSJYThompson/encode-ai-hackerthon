import requests
import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt

def fetch_historical_data(coin_id: str, vs_currency: str, days: int = 1) -> pd.DataFrame:
    """
    Fetch historical data for a given cryptocurrency from CoinGecko.
    
    This function uses the market_chart endpoint with fallbacks for different time ranges.
    
    Args:
        coin_id (str): The CoinGecko ID of the cryptocurrency (e.g. 'bitcoin').
        vs_currency (str): The target currency (typically fiat, e.g. 'usd' or 'gbp').
        days (int): Number of days to fetch (default=1 for the last 24 hours).
    
    Returns:
        pd.DataFrame: DataFrame with columns 'timestamp' and 'price'.
    """
    timestamps = []
    prices_list = []
    prices = []

    # Try the market_chart endpoint
    market_chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    print(f"[DEBUG] Requesting data for {coin_id} using market_chart endpoint.")
    response = requests.get(market_chart_url, params=params)
    data = response.json()
    prices = data.get("prices", [])

    # If no data returned, try the market_chart/range endpoint (1-day)
    if not prices:
        print("[DEBUG] No data from market_chart endpoint; trying market_chart/range for a 24-hour window.")
        end_time = int(time.time())
        start_time = end_time - 86400  # last 24 hours
        range_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range"
        params = {"vs_currency": vs_currency, "from": start_time, "to": end_time}
        response = requests.get(range_url, params=params)
        data = response.json()
        prices = data.get("prices", [])
        # If still empty, try a 2-day range and filter for the last 24 hours.
        if not prices:
            print("[DEBUG] Still no data; trying a 2-day range and filtering to last 24 hours.")
            end_time = int(time.time())
            start_time = end_time - 2 * 86400  # 2-day window
            params = {"vs_currency": vs_currency, "from": start_time, "to": end_time}
            response = requests.get(range_url, params=params)
            data = response.json()
            prices = data.get("prices", [])
            # Filter only points within the last 24 hours.
            lower_bound = (end_time - 86400) * 1000  # timestamps in ms
            prices = [point for point in prices if point[0] >= lower_bound]

    print(f"[DEBUG] Retrieved {len(prices)} historical price points for {coin_id}.")
    
    # Build a DataFrame if data was retrieved
    for ts, price in prices:
        timestamps.append(datetime.datetime.fromtimestamp(ts / 1000))
        prices_list.append(price)
    
    df = pd.DataFrame({
        "timestamp": timestamps,
        "price": prices_list
    })
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def fetch_conversion_series_fiat_to_crypto(coin_id: str, vs_currency: str, days: int = 1) -> pd.DataFrame:
    """
    Get fiat-to-crypto conversion rate by inverting the crypto-to-fiat price data.
    
    Args:
        coin_id (str): The CoinGecko ID of the cryptocurrency (e.g. 'bitcoin').
        vs_currency (str): The fiat currency (e.g. 'usd').
        days (int): Number of days to fetch.
    
    Returns:
        pd.DataFrame: DataFrame with columns 'timestamp' and 'fiat_to_crypto_rate'.
    """
    df = fetch_historical_data(coin_id, vs_currency, days)
    if df.empty:
        return df
    # Invert the prices: fiat_to_crypto_rate = 1 / crypto_to_fiat_price
    df['fiat_to_crypto_rate'] = 1 / df['price']
    return df[['timestamp', 'fiat_to_crypto_rate']]

def fetch_conversion_series_crypto_to_crypto(source_id: str, target_id: str, vs_currency: str, days: int = 1) -> pd.DataFrame:
    """
    Compute crypto-to-crypto conversion rate using prices in a common fiat currency.
    
    Fetch historical price data for both cryptocurrencies and then compute:
        conversion_rate = price_source / price_target.
    
    Args:
        source_id (str): The CoinGecko ID of the source cryptocurrency.
        target_id (str): The CoinGecko ID of the target cryptocurrency.
        vs_currency (str): The fiat currency (e.g. 'usd').
        days (int): Number of days to fetch.
    
    Returns:
        pd.DataFrame: DataFrame with columns 'timestamp' and 'crypto_conversion_rate'.
    """
    # Get historical data for both coins
    df_source = fetch_historical_data(source_id, vs_currency, days)
    df_target = fetch_historical_data(target_id, vs_currency, days)
    
    if df_source.empty or df_target.empty:
        print("[DEBUG] One or both data series are empty.")
        return pd.DataFrame()
    
    # Merge on the timestamp. Depending on API data frequency,
    # you may need to align or interpolate the timestamps.
    df_merged = pd.merge_asof(df_source.sort_values('timestamp'),
                              df_target.sort_values('timestamp'),
                              on='timestamp', direction='nearest',
                              suffixes=('_source', '_target'))
    
    # Calculate conversion rate: how many units of target per one unit of source
    df_merged['crypto_conversion_rate'] = df_merged['price_source'] / df_merged['price_target']
    return df_merged[['timestamp', 'crypto_conversion_rate']]

def main():
    # For demonstration, you can change these parameters:
    coin_id = "bitcoin"
    fiat_currency = "gbp"
    days = 1
    
    # --- Crypto to Fiat conversion (original use case) ---
    df_history = fetch_historical_data(coin_id, fiat_currency, days)
    if df_history.empty:
        print("No historical data was retrieved for crypto-to-fiat.")
    else:
        print("Crypto to Fiat (Price):")
        print(df_history.head())
        plt.figure(figsize=(10, 5))
        plt.plot(df_history["timestamp"], df_history["price"], marker='o', linestyle='-')
        plt.xlabel("Time")
        plt.ylabel(f"Price ({fiat_currency.upper()})")
        plt.title(f"{coin_id.capitalize()} Price Over the Last 24 Hours")
        plt.grid(True)
        plt.show()
    
    # --- Fiat to Crypto conversion ---
    df_fiat_to_crypto = fetch_conversion_series_fiat_to_crypto(coin_id, fiat_currency, days)
    if df_fiat_to_crypto.empty:
        print("No historical data was retrieved for fiat-to-crypto.")
    else:
        print("Fiat to Crypto (Inverted Rate):")
        print(df_fiat_to_crypto.head())
        plt.figure(figsize=(10, 5))
        plt.plot(df_fiat_to_crypto["timestamp"], df_fiat_to_crypto["fiat_to_crypto_rate"], marker='o', linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Crypto per Fiat Unit")
        plt.title(f"{fiat_currency.upper()} to {coin_id.capitalize()} Conversion Rate Over the Last 24 Hours")
        plt.grid(True)
        plt.show()
    
    # --- Crypto to Crypto conversion ---
    # Example: Converting Ethereum to Bitcoin.
    source_id = "ethereum"
    target_id = "bitcoin"
    df_crypto_to_crypto = fetch_conversion_series_crypto_to_crypto(source_id, target_id, fiat_currency, days)
    if df_crypto_to_crypto.empty:
        print("No historical data was retrieved for crypto-to-crypto.")
    else:
        print("Crypto to Crypto (Conversion Rate - Source/Target):")
        print(df_crypto_to_crypto.head())
        plt.figure(figsize=(10, 5))
        plt.plot(df_crypto_to_crypto["timestamp"], df_crypto_to_crypto["crypto_conversion_rate"], marker='o', linestyle='-')
        plt.xlabel("Time")
        plt.ylabel("Conversion Rate")
        plt.title(f"{source_id.capitalize()} to {target_id.capitalize()} Conversion Rate Over the Last 24 Hours")
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    main()
