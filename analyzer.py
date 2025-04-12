from data_fetcher import MarketDataFetcher
from predictor import ExchangeRatePredictor
import numpy as np

class TokenSwapAnalyzer:
    def __init__(self):
        self.fetcher = MarketDataFetcher()
        self.predictor = ExchangeRatePredictor()

    def compare_tokens(self, from_token, to_token):
        data_from = self.fetcher.get_token_data(from_token)
        data_to = self.fetcher.get_token_data(to_token)

        #print("Debug:", data_from["raw_chart_data"])

        if not data_from or not data_to:
            return "❌ Error fetching data. Please try again."

        # Calculate exchange rate
        rate = data_from['price'] / data_to['price']

        # Rule-based analysis
        advice = self.make_decision(data_from, data_to)

        report = f"""
        📊 Token Swap Report: {from_token.upper()} → {to_token.upper()}
        
        🔁 Current Rate:
          1 {from_token.upper()} = {rate:.4f} {to_token.upper()}
        
        💹 {from_token.upper()}:
          Price: ${data_from['price']:.2f}
          24h Change: {data_from['price_change_24h']}%
          Volatility: {data_from['volatility']}%
        
        💹 {to_token.upper()}:
          Price: ${data_to['price']:.2f}
          24h Change: {data_to['price_change_24h']}%
          Volatility: {data_to['volatility']}%
        
        🧠 AI Insight:
        {advice}
        """
        return report

    def make_decision(self, data_from, data_to):
        # Extract last 24h prices
        #prices_from = [p[1] for p in data_from['raw_chart_data']['prices']]
        #prices_to = [p[1] for p in data_to['raw_chart_data']['prices']]
        # I changed some stuff here because there is no prices subindex now for some reason
        prices_from = np.array(data_from['raw_chart_data'])[:, 1]
        prices_to =  np.array(data_to['raw_chart_data'])[:, 1]

        # Predict next-hour exchange rate
        predicted = self.predictor.predict_next_rate(prices_from, prices_to)

        # Compare with current
        current = data_from['price'] / data_to['price']
        diff = predicted - current
        percent_diff = (diff / current) * 100

        # Decision logic
        if percent_diff > 1:
            return f"⏳ Prediction: Rate expected to improve by {percent_diff:.2f}%. You may wait before swapping."
        elif percent_diff < -1:
            return f"✅ Prediction: Rate may worsen by {abs(percent_diff):.2f}%. Good time to convert now."
        else:
            return f"ℹ️ Prediction: Minimal change ({percent_diff:.2f}%). Convert if needed, or wait for better trend."

