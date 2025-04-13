import streamlit as st
import requests
import json

import requests

url = "https://free-rpc.nethermind.io/mainnet-juno/"
payload = {
    "jsonrpc": "2.0",
    "method": "starknet_blockHashAndNumber",
    "id": 1
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
block_number = response.json()["result"]["block_number"]
block_hash = response.json()["result"]["block_hash"]

st.title("Starknet (running on Nethermind) information")

st.text(f"Status code: {response.status_code}")
st.text(f"Most recent block number: {block_number}")
st.text(f"Hash for the most recent block: {block_hash}")