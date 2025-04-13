import streamlit as st
import requests
import json

# Define your API key (replace with your actual key)
api_key = st.secrets["VOYAGER_ONLINE_API_KEY"]  # Insert your actual API key here

# Define the RPC URL for the Nethermind node
rpc_url = "https://rpc.nethermind.io/mainnet-juno"

headers = {
    'x-apikey': st.secrets["VOYAGER_ONLINE_API_KEY"],
    'Content-Type': 'application/json'
}

url = "https://rpc.nethermind.io/mainnet-juno"

payload = json.dumps({
    "jsonrpc": "2.0",
    "method": "starknet_blockHashAndNumber",
    "params": [],
    "id": 0
})
headers = {
    'x-apikey': 'YOUR API KEY',
    'Content-Type': 'application/json'
}

# Function to send JSON-RPC requests with the API key in headers
def send_rpc_request(method, params=None):
    if params is None:
        params = []

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    payload = {
        "jsonrpc": "2.0",
        "method": "juno_version",
        "id": 0
    }

    response = requests.post(rpc_url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to retrieve data from node"}


# Streamlit UI
st.title("StarkNet Data Query Dashboard")

# Introduction for StarkNet Methods
st.markdown("""
### Welcome to the StarkNet Data Query Dashboard
This dashboard allows you to view information from the StarkNet blockchain network without needing to input specific values.
You can choose from a variety of queries below to view block data, gas fees, transaction information, and more.

Please select one of the following options to begin.
""")

# Select StarkNet data to query
starknet_option = st.selectbox(
    "Select StarkNet information to query:",
    [
        "Latest Block Data",
        "StarkNet Block Data by Hash",
        "StarkNet Gas Fees",
        "StarkNet Transaction Details"
    ]
)

button = st.button("Retrieve data")

current_task = st.empty()

# Handle the selected StarkNet option
if starknet_option == "Latest Block Data":
    st.markdown("""
    ### Latest Block Data
    This section shows information about the most recent block in the StarkNet network, including the block hash and block number.

    """)
    if button:
        current_task = st.text("Fetching data...")
        # Fetch latest block data
        result = send_rpc_request("starknet_blockHashAndNumber", [])
        current_task = st.empty()
        st.write(result)

elif starknet_option == "StarkNet Block Data by Hash":
    st.markdown("""
    ### StarkNet Block Data by Hash
    This section allows you to retrieve details of a specific block using its block hash. The block data will include information such as block number, hash, and more.

    Fetching data...
    """)
    # Example: Block hash data
    block_hash = "0x167ba7aac2d97b82a802a820fa96d00925167a74748ffbc9201e46dbd2f46a5"  # Replace with an actual block hash
    if button:
        result = send_rpc_request("starknet_getBlockByHash", [block_hash])
        st.write(result)

elif starknet_option == "StarkNet Gas Fees":
    st.markdown("""
    ### StarkNet Gas Fees
    This section provides the current gas price in the StarkNet network. Gas fees are required for transactions and smart contract execution.

    Fetching data...
    """)
    # Fetch current StarkNet gas price
    result = send_rpc_request("starknet_gasPrice")
    st.write(result)

elif starknet_option == "StarkNet Transaction Details":
    st.markdown("""
    ### StarkNet Transaction Details
    Here, you can view detailed information about a specific StarkNet transaction, including sender, receiver, and transaction status.

    Fetching data...
    """)
    # Example: Transaction hash data
    tx_hash = "0x5e4a9d4f7f4ac09bccebed72d4d3275d9b95795ecf3b5894d62d8da946f4512e"  # Replace with an actual transaction hash
    result = send_rpc_request("starknet_getTransactionReceipt", [tx_hash])
    st.write(result)