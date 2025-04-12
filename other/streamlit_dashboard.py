import streamlit as st

import get_transaction_data

st.title("Ethereum Transaction Viewer")

txs = get_transaction_data.get_transaction_data()

for tx in txs[:10]:  # limit to recent 10
    st.write({
        "From": tx["from"],
        "To": tx["to"],
        "Value (ETH)": int(tx["value"]) / 1e18,
        "Gas Used": tx["gasUsed"],
        "Status": "Success" if tx["isError"] == "0" else "Fail"
    })