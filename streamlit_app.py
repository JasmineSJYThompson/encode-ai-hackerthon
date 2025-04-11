import streamlit as st
from analyzer import TokenSwapAnalyzer

analyzer = TokenSwapAnalyzer()

# Streamlit sidebar
with st.sidebar:
    st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...)")

    function_selection = st.sidebar.selectbox(
        "Please select a function",
        ("Generate Report", "Exchange Rate Calculator"))

    from_token = st.text_input("Enter token we are converting from", value="bitcoin")
    to_token = st.text_input("Enter token we are converting to", value="ethereum")

    if function_selection == "Generate Report":
        generate_report_button = st.button("Generate risk report")

    if function_selection == "Exchange Rate Calculator":
        exchange_rate_button = st.button("Generate ")

# Streamlit main body
title_text = {"Generate Report": "🔍 DeFi Token Risk Analyzer", "Exchange Rate Calculator": "Exchange Rate Calculator"}
st.title(title_text[function_selection])
current_task = st.empty()

if generate_report_button:
    current_task.text("Writing report...")
    report = analyzer.compare_tokens(from_token, to_token)  # BTC → ETH
    current_task.empty()
    st.write(report)
