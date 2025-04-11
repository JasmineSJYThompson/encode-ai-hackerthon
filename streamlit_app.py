import streamlit as st
from analyzer import TokenSwapAnalyzer

analyzer = TokenSwapAnalyzer()

# Streamlit sidebar
with st.sidebar:
    st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...) and generate a risk report.")

    from_token = st.text_input("Enter token we are converting from", value="bitcoin")
    to_token = st.text_input("Enter token we are converting to", value="ethereum")

    generate_report_button = st.button("Generate Report")

# Streamlit main body
st.title("🔍 DeFi Token Risk Analyzer")
current_task = st.empty()

if generate_report_button:
    current_task.text("Writing report...")
    report = analyzer.compare_tokens(from_token, to_token)  # BTC → ETH
    current_task.empty()
    st.write(report)
