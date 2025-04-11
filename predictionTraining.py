import requests
import time

#   Used coinGecko API to fetch crypto data

def get_all_crypto_prices(vs_currency='usd', per_page=250):
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    all_data = []
    page = 1

    while True:
        params = {
            'vs_currency': vs_currency,
            'order': 'market_cap_desc',
            'per_page': per_page,
            'page': page,
            'sparkline': False
        }
        
        
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"Requesting page {page}... Status code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Error fetching page {page}: {response.status_code}")
                break  
            
            # Converting the response to json
            data = response.json()

            if not data:
                print("No more data, exiting.")
                break

           
            all_data.extend(data)
            page += 1  
            
           
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            break
    return all_data
cryptos = get_all_crypto_prices()
# Printing top 10 crypto price
for coin in cryptos[:10]:   
    print(f"{coin['name']} ({coin['symbol'].upper()}): {coin['current_price']} USD")
