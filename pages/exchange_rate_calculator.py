import streamlit as st
from utils.converter import DeFiConverter

# Streamlit sidebar
with st.sidebar:
    st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...)")
    
    coins = ('BTC', 'ETH', 'USDC', 'USDT', 'BNB', 'SOL',
             'ADA', 'MATIC', 'DOT', 'LTC', 'GBP', 'USD')

    from_token = st.selectbox(
    "Enter token we are converting from", index=0,
    coins)
    to_token = st.selectbox(
    "Enter token we are converting to", index=1,
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
        st.subheader(f"{number_tokens_from:.4f} {from_token} becomes {number_tokens_to:.4f} {to_token}")
    except ValueError as e:
        st.error(e)
        current_task.empty()
    except Exception as e:
        st.error(e)
        current_task.empty()

