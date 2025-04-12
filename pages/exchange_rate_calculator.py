import streamlit as st
from utils.converter import DeFiConverter

# Streamlit sidebar
with st.sidebar:
    st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...)")
    
    coins = ('BTC', 'ETH', 'USDC', 'USDT', 'BNB', 'SOL',
             'ADA', 'MATIC', 'DOT', 'LTC', 'GBP', 'USD')

    from_token = st.selectbox(
    "Enter token we are converting from",
    coins)
    to_token = st.selectbox(
        "Enter token we are converting to",
        coins)

    number_tokens_from = st.number_input("Insert number of tokens", value=1, min_value=0)

    button = st.button("Generate exchange rate")

# Streamlit main body
st.title("📈 Exchange Rate Calculator")
current_task = st.empty()

if button:
    current_task.text("Retrieving data...")
    try:
        converter = DeFiConverter()
        number_tokens_to = converter.convert_currency(number_tokens_from, from_token, to_token)
        current_task.empty()
        st.subheader(f"{number_tokens_from:.2f} {from_token} becomes {number_tokens_to:.2f} {to_token}")
    except ValueError as e:
        st.write(e)
        current_task.empty()

