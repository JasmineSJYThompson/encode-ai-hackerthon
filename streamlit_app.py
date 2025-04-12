import streamlit as st
from analyzer import TokenSwapAnalyzer
from data_fetcher2 import MarketDataFetcher

analyzer = TokenSwapAnalyzer()
data_fetcher = MarketDataFetcher()

# Streamlit sidebar
with st.sidebar:
    function_selection = st.sidebar.selectbox(
        "Please select a function",
        ("Generate Report", "Exchange Rate Calculator"))

    if function_selection in ("Generate Report", "Exchange Rate Calculator"):
        st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...)")

        from_token = st.text_input("Enter token we are converting from", value="bitcoin")
        to_token = st.text_input("Enter token we are converting to", value="ethereum")

    number_tokens_from = 1
    if function_selection == "Exchange Rate Calculator":
        number_tokens_from = st.number_input("Insert number of tokens")

    button = st.empty()
    if function_selection == "Generate Report":
        button = st.button("Generate risk report")
    elif function_selection == "Exchange Rate Calculator":
        button = st.button("Generate exchange rate")

# Streamlit main body
title_text = {"Generate Report": "🔍 DeFi Token Risk Analyzer", "Exchange Rate Calculator": "Exchange Rate Calculator"}
st.title(title_text[function_selection])
current_task = st.empty()

if button:
    if function_selection == "Generate Report":
        current_task.text("Writing report...")
        report = analyzer.compare_tokens(from_token, to_token)  # BTC → ETH
        current_task.empty()
        st.write(report)
    elif function_selection == "Exchange Rate Calculator":
        current_task.text("Retrieving data...")
        price_in = data_fetcher.get_token_data(from_token)["price"]
        price_out = data_fetcher.get_token_data(to_token)["price"]
        rate = price_in/price_out
        current_task.empty()
        st.subheader(f"{number_tokens_from:.2f} {from_token}")
        st.subheader(f"becomes {number_tokens_from*rate:.2f} {to_token}")