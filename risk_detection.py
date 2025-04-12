import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("integrated_data.csv", parse_dates=["timestamp"])
print("Integrated Data from CSV:")
print(df)
df['price_change'] = df['ethereum_price'].diff().fillna(0)
features = ['price_change', 'transaction_count', 'gas_used', 'difficulty', 'ethereum_24h_change']
missing_features = [f for f in features if f not in df.columns]
if missing_features:
    print(f"Warning: Missing features: {missing_features}")
    features = [f for f in features if f in df.columns]
df[features] = df[features].fillna(0)

# Create an Isolation Forest model and fit using the selected features
model = IsolationForest(contamination=0.1, random_state=42)
df['anomaly'] = model.fit_predict(df[features])

print("Risk Detection Results:")
print(df[['timestamp', 'ethereum_price'] + features + ['anomaly']])
