import pandas as pd
from sklearn.ensemble import IsolationForest

# 在指定时间点上进行风险检测
def detect_risk_at_time(target_time, csv_path="data/mock_integrated_data.csv"):
    df = pd.read_csv(csv_path, parse_dates=["timestamp"])
    df['price_change'] = df['ethereum_price'].diff().fillna(0)
    features = ['price_change', 'transaction_count', 'gas_used', 'difficulty', 'ethereum_24h_change']
    features = [f for f in features if f in df.columns]
    df[features] = df[features].fillna(0)

    model = IsolationForest(contamination=0.1, random_state=42)
    df['anomaly'] = model.fit_predict(df[features])

    df['time_diff'] = (df['timestamp'] - pd.to_datetime(target_time)).abs()
    row = df.sort_values('time_diff').iloc[0]
    is_risky = row['anomaly'] == -1
    return is_risky, row.to_dict()
