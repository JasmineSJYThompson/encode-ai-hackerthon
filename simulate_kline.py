import numpy as np
import pandas as pd
import mplfinance as mpf
import datetime
import random

def generate_dense_kline_data(num_bars=200, start_price=100.0, seed=42, interval_minutes=2):
    random.seed(seed)
    np.random.seed(seed)

    k_data = {
        'Date': [],
        'Open': [],
        'High': [],
        'Low': [],
        'Close': [],
        'Volume': []
    }

    current_price = start_price
    base_datetime = datetime.datetime.now()

    for i in range(num_bars):
        current_datetime = base_datetime + datetime.timedelta(minutes=i * interval_minutes)

        open_price = current_price + random.uniform(-1, 1)
        
        price_change = random.uniform(-3, 3)
        close_price = open_price + price_change

        high_price = max(open_price, close_price) + random.uniform(0, 2)
        low_price = min(open_price, close_price) - random.uniform(0, 2)
        if low_price < 0:
            low_price = 0.1

        volume = random.randint(100, 5000)

        k_data['Date'].append(current_datetime)
        k_data['Open'].append(round(open_price, 2))
        k_data['High'].append(round(high_price, 2))
        k_data['Low'].append(round(low_price, 2))
        k_data['Close'].append(round(close_price, 2))
        k_data['Volume'].append(volume)

        current_price = close_price

    df = pd.DataFrame(k_data)
    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)

    return df

if __name__ == '__main__':
    df_kline = generate_dense_kline_data(num_bars=200, start_price=100.0, seed=42, interval_minutes=2)
    print(df_kline.head(10))

    mpf.plot(
        df_kline,
        type='candle',
        mav=(5, 10),
        volume=True,
        title='Simulate Kline Data',
        style='yahoo',
        figsize=(12, 7)
    )

    df_kline.to_csv('simulate_kline_data.csv')





