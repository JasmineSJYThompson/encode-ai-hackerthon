from web3 import Web3

# Cloudflare's free Ethereum RPC
w3 = Web3(Web3.HTTPProvider("https://cloudflare-eth.com"))

print("Connected:", w3.is_connected())

# Get the latest block number
latest_block = w3.eth.block_number
print(f"Latest Block: {latest_block}")

# Get block details for the latest block
block_info = w3.eth.get_block(latest_block)
print(f"Block Info: {block_info}")

# Extract unique addresses from the transactions
addresses = set()
for tx in block_info['transactions']:
    addresses.add(tx['from'])
    addresses.add(tx['to'])

# Calculate a simple risk score (higher active nodes = lower risk)
active_addresses = len(addresses)
block_transaction_count = len(block_info['transactions'])
risk_score = 1 - (active_addresses / block_transaction_count)  # Simple inverse relation

print(f"Active Addresses: {active_addresses}, Risk Score: {risk_score}")