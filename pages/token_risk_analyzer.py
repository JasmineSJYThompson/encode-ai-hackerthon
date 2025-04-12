import streamlit as st
from utils.analyzer import TokenSwapAnalyzer

# Streamlit sidebar
with st.sidebar:
    st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...)")

    from_token = st.text_input("Enter token we are converting from", value="BTC")
    to_token = st.text_input("Enter token we are converting to", value="ETH")

    button = st.button("Generate risk report")

# Streamlit main body
st.title("🔍 DeFi Token Risk Analyzer")

current_task = st.empty()

if button:
    current_task.text("Writing report...")
    analyzer = TokenSwapAnalyzer()
    report = analyzer.compare_tokens(from_token, to_token)  # BTC → ETH
    current_task.empty()
    st.write(report)
