import pandas as pd
import numpy as np

df = pd.read_csv('simulate_kline_data.csv', parse_dates=['Date'])
df = df.rename(columns={'Date': 'timestamp', 'Close': 'ethereum_price'})

df['transaction_count'] = np.random.randint(100, 500, size=len(df))
df['gas_used'] = np.random.randint(1_000_000, 15_000_000, size=len(df))
df['difficulty'] = np.random.randint(1_000_000_000_000, 9_000_000_000_000, size=len(df))
df['ethereum_24h_change'] = np.random.normal(0, 2, size=len(df))

columns = ['timestamp', 'ethereum_price', 'transaction_count', 'gas_used', 'difficulty', 'ethereum_24h_change']
df = df[columns]

df.to_csv('mock_integrated_data.csv', index=False)
