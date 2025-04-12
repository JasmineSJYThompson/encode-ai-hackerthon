import requests
import numpy as np

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Calculated market risk on scale of 1 to 100 based on market capitalization, volatility, Price Change Percentage in last 24 hr
def fetch_coin_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',  # usd
        'order': 'market_cap_desc', 
        'per_page': 10,  # top 10 coins
        'page': 1 
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if response.status_code != 200:
        print("Error fetching data from CoinGecko")
        return []
    
    return data

def calculate_market_risk(data):
    market_caps = [coin['market_cap'] for coin in data]
    price_changes = [coin['price_change_percentage_24h'] for coin in data]
    
    # Calculate market cap risk (the lower the market cap, the higher the risk)
    market_cap_risk = np.mean([np.log(market_cap) for market_cap in market_caps if market_cap > 0])  #
    
    # Calculate volatility risk (higher price change percentage indicates higher risk)
    volatility_risk = np.mean([abs(change) for change in price_changes])  
    
    # Normalize the values to avoid extreme unscaled values
    normalized_market_cap_risk = np.clip(market_cap_risk, -5, 5)  
    normalized_volatility_risk = np.clip(volatility_risk, 0, 100)  
    
    # Calculate overall risk
    risk = (normalized_market_cap_risk * 0.5) + (normalized_volatility_risk * 0.5)
    
    min_risk = 0.01
    max_risk = 10.0
    scaled_risk = (risk - min_risk) / (max_risk - min_risk) * 99 + 1
    
    return int(np.clip(scaled_risk, 1, 100))  # Return the risk value as an integer

def main():
    print("Fetching data from CoinGecko...")
    data = fetch_coin_data()
    
    if not data:
        print("No data available to calculate the risk.")
        return None
    
    print("Calculating market risk...")
    risk = calculate_market_risk(data)
    
    print(f"Current crypto market risk level: {risk}/100")
    
    return risk  # Return the risk value

# Initialize Firebase Admin SDK
cred = credentials.Certificate("APK/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://myaiagent-45599-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Reference to the 'RiskValue' node in the Firebase Realtime Database
users_ref = db.reference('RiskValue')

def send_risk_to_firebase(risk):
    try:
        if risk is not None:
            # Send the calculated risk value to Firebase
            users_ref.set(risk)
            print(f"Successfully sent the risk value: {risk} to Firebase.")
        else:
            print("No risk value to send.")
    except Exception as e:
        print(f"Error occurred while sending to Firebase: {e}")

if __name__ == "__main__":
    market_risk = main()
    
    # Send the risk value to Firebase if it exists
    send_risk_to_firebase(market_risk)
