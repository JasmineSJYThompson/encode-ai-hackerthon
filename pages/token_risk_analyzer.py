import streamlit as st
from utils.analyzer import TokenSwapAnalyzer
import time

MOCK_REPORT=True

# Streamlit sidebar
with st.sidebar:
    st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...)")

    from_token = st.text_input("Enter token we are converting from", value="BTC")
    to_token = st.text_input("Enter token we are converting to", value="ETH")

    button = st.button("Generate risk report")

# Streamlit main body
st.title("🔍 DeFi Token Risk Analyzer")

current_task = st.empty()

def save_data(file, text):
    with open(file, "w", encoding="utf-8") as f:
        f.write(text)

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()
    return content

if button:
    current_task.text("Writing report...")
    analyzer = TokenSwapAnalyzer()
    if MOCK_REPORT:
        time.sleep(1)
        report = load_data("data/report.txt")
    else:
        report = analyzer.compare_tokens(from_token, to_token)  # BTC → ETH
    current_task.empty()
    st.write(report)
