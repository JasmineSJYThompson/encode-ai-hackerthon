import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("mock_integrated_data.csv", parse_dates=["timestamp"])
df['price_change'] = df['ethereum_price'].diff().fillna(0)
features = ['price_change', 'transaction_count', 'gas_used', 'difficulty', 'ethereum_24h_change']
df[features] = df[features].fillna(0)

model = IsolationForest(contamination=0.1, random_state=42)
df['anomaly'] = model.fit_predict(df[features])

def check_risk(timestamp_str):
    try:
        timestamp = pd.to_datetime(timestamp_str)
    except ValueError:
        print("❌ Invalid timestamp format. Please use something like '2025-04-12 15:34:07'")
        return

    df['time_diff'] = (df['timestamp'] - timestamp).abs()
    closest_row = df[df['time_diff'] <= pd.Timedelta(minutes=2)].sort_values('time_diff').head(1)

    if closest_row.empty:
        print(f"⚠️ No matching data found near {timestamp_str}")
        return

    is_risky = int(closest_row['anomaly'].values[0]) == -1
    real_timestamp = closest_row['timestamp'].values[0]
    price = closest_row['ethereum_price'].values[0]

    print(f"\n🕒 Attempting trade near {timestamp} (matched to {real_timestamp})")
    print(f"Current price: ${price:.2f}")
    if is_risky:
        print("🚨 ALERT: Risk detected! It is not recommended to trade at this time.")
    else:
        print("✅ Safe to trade. No risk detected.")

print("===== Risk Alert Demo (Fixed Timepoints) =====")
normal_time = df[df['anomaly'] == 1].iloc[10]['timestamp']
risky_time = df[df['anomaly'] == -1].iloc[0]['timestamp']
check_risk(normal_time)
check_risk(risky_time)

# Interactive mode
print("\n===== Interactive Risk Check =====")
print("Enter a timestamp (e.g. 2025-04-12 15:34:07) to check if it's safe to trade.")
print("Type 'exit' to quit.")

while True:
    user_input = input("\n🕐 Enter timestamp: ").strip()
    if user_input.lower() == 'exit':
        print("👋 Exiting risk check.")
        break
    check_risk(user_input)
