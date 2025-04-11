import requests
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

    # Used coinGecko API to fetch crypto data
    # Fetched user emails entered through application

cred = credentials.Certificate("APK/firebase_key.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://myaiagent-45599-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Reference to the 'email' node in the Firebase Realtime Database
users_ref = db.reference('Users')

try:
    # Fetch data from the 'USERS' node
    users_data = users_ref.get()

    # Print out the data to see the structure
    print("Raw data from Firebase Realtime DB:")
    print(users_data)
    
    if users_data is None:
        print("No data found at the 'USERS' reference.")
    else:
        print("Data from Firebase Realtime DB:")
        
        # Check if the data is a dictionary
        if isinstance(users_data, dict):
            # Iterate through the children of USERS (each child has a random key)
            for user_key, user_value in users_data.items():
                # Print the email of each user
                print(f"User ID: {user_key}, Email: {user_value['email']}")
        else:
            print("Error: The data is not in the expected format.")
        
except Exception as e:
    print(f"Error occurred: {e}")


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
