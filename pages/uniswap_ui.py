import streamlit as st
import pandas as pd
from utils.risk import detect_risk_at_time

st.set_page_config(page_title="Uniswap Demo with Risk Detection", page_icon="💱", layout="centered")

@st.cache_data
def load_data():
    df = pd.read_csv("data/mock_integrated_data.csv", parse_dates=["timestamp"])
    return df

df = load_data()
timestamps = df["timestamp"]
default_time = timestamps.iloc[-1].to_pydatetime()

st.markdown("""
<style>
.title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 24px;
    text-align: center;
}
.swap-box {
    background-color: #f9f9f9;
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    width: 100%;
    max-width: 420px;
    margin: auto;
}
.token-row {
    background-color: white;
    border-radius: 12px;
    padding: 12px 16px;
    border: 1px solid #eee;
    margin-bottom: 16px;
}
.token-label {
    font-size: 14px;
    font-weight: 500;
    color: #666;
    margin-bottom: 6px;
}
.token-select {
    float: right;
    background: #f0f0f0;
    padding: 4px 10px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 14px;
    margin-left: 10px;
    color: #333;
}
.rate-text {
    text-align: right;
    font-size: 13px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">💱 Crypto Swap (Risk Demo Mode)</div>', unsafe_allow_html=True)

selected_time = st.slider(
    "🕒 Select a timestamp (demo mode)",
    min_value=timestamps.min().to_pydatetime(),
    max_value=timestamps.max().to_pydatetime(),
    value=default_time,
    format="YYYY-MM-DD HH:mm:ss"
)

df['time_diff'] = (df['timestamp'] - pd.to_datetime(selected_time)).abs()
closest_row = df.sort_values('time_diff').iloc[0]
eth_price = float(closest_row["ethereum_price"])

#st.markdown('<div class="swap-box">', unsafe_allow_html=True)

st.markdown('<div class="token-row">', unsafe_allow_html=True)
st.markdown('<div class="token-label">From <span class="token-select">USDC</span></div>', unsafe_allow_html=True)
usdc_amount = st.number_input("USDC Input", min_value=0.0, step=1.0, value=100.0, key="usdc", label_visibility="collapsed")
st.markdown('</div>', unsafe_allow_html=True)

eth_amount = usdc_amount / eth_price

st.markdown('<div class="token-row">', unsafe_allow_html=True)
st.markdown('<div class="token-label">To <span class="token-select">ETH</span></div>', unsafe_allow_html=True)
st.markdown(f"""
<div style="
    background-color: #f1f3f5;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 20px;
    font-weight: 600;
    color: #333;
    margin-top: -10px;
">
    {eth_amount:.6f}
</div>
""", unsafe_allow_html=True)
st.markdown(f'<div class="rate-text">1 ETH = <strong>{eth_price:.2f} USDC</strong></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔄 Swap (Simulated)", key="swap"):
    is_risk, row_data = detect_risk_at_time(selected_time)
    if is_risk:
        st.error("🚨 Risk Detected at selected time: Transaction blocked!")
        with st.expander("📊 View Risk Data"):
            st.json(row_data)
    else:
        st.success(f"✅ Swapped {usdc_amount:.2f} USDC for {eth_amount:.6f} ETH safely.")

st.markdown('</div>', unsafe_allow_html=True)
