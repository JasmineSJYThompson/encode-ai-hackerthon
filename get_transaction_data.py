import requests

ETHERSCAN_API_KEY = "<add your own etherscan api key>"
address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'

def get_transaction_data():
    url = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&sort=desc&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    txs = response.json()["result"]
    return txs