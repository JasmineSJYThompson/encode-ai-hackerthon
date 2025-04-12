import pandas as pd
from connect_to_infura import get_onchain_data
from get_market_data import get_offchain_market_data

# Get on-chain and off-chain data
onchain_data = get_onchain_data()
offchain_data = get_offchain_market_data()

# Combine the data into a dictionary 
data = {
     'timestamp': [onchain_data['timestamp']],    
    'ethereum_price': [offchain_data['ethereum_price']],
    'block_number': [onchain_data['block_number']],
    'gas_used': [onchain_data['gasUsed']],
    'gas_limit': [onchain_data['gasLimit']],
    'transaction_count': [onchain_data['transaction_count']],
    'difficulty': [onchain_data['difficulty']],
    'ethereum_market_cap': [offchain_data['ethereum_market_cap']],
    'ethereum_24h_vol': [offchain_data['ethereum_24h_vol']],
    'ethereum_24h_change': [offchain_data['ethereum_24h_change']]
}

df = pd.DataFrame(data)
print("Integrated Data:")
print(df)

# Save the integrated data to CSV
df.to_csv("integrated_data.csv", index=False)
