import requests

def get_offchain_market_data():
    coingecko_url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'ethereum',
        'vs_currencies': 'usd',
        'include_market_cap': 'true',
        'include_24hr_vol': 'true',
        'include_24hr_change': 'true'
    }
    # Make the request to fetch the current price of Ethereum in USD
    response = requests.get(coingecko_url, params=params)
    if response.status_code == 200:
        price_data = response.json()
        eth_data = price_data.get('ethereum', {})
        return {
            'ethereum_price': eth_data.get('usd', None),
            'ethereum_market_cap': eth_data.get('usd_market_cap', None),
            'ethereum_24h_vol': eth_data.get('usd_24h_vol', None),
            'ethereum_24h_change': eth_data.get('usd_24h_change', None)
        }
    else:
        raise Exception("Failed to retrieve market data from CoinGecko.")
