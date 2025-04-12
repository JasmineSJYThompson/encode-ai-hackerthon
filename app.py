# app.py (global entry point)
import streamlit as st
from utils.converter import DeFiConverter

# Optional: You can define common global UI here
st.title("💫 ArgusFi App")
st.sidebar.header("App Controls")

converter = DeFiConverter()
st.pyplot(fig = converter.plot_history("btc", "usd", days=1))

# Maybe include some global settings, but don't manage the pages directly
