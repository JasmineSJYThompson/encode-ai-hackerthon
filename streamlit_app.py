from analyzer import TokenSwapAnalyzer

analyzer = TokenSwapAnalyzer()

# Streamlit UI
st.title("🔍 DeFi Token Risk Analyzer")
st.markdown("Enter two token names (e.g., bitcoin, ethereum, etc...) and generate a risk report.")

from_token = st.text_input("Enter token we are converting from", value="bitcoin")
to_token = st.text_input("Enter token we are converting to", value="ethereum")

current_task = st.empty()

if st.button("Generate Report"):
    current_task.text("Writing report...")
    report = analyzer.compare_tokens(from_token, to_token)  # BTC → ETH
    current_task.empty()
    st.write(report)