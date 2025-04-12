import numpy as np
from sklearn.linear_model import LinearRegression

class ExchangeRatePredictor:
    def __init__(self):
        self.model = LinearRegression()

    def predict_next_rate(self, prices_from, prices_to):
        # convert to exchange rate series: rate = from / to
        rates = np.array([f / t for f, t in zip(prices_from, prices_to)])
        X = np.arange(len(rates)).reshape(-1, 1)
        y = rates

        # train model
        self.model.fit(X, y)

        # predict for the next point (1 hour ahead = +1 index)
        next_index = [[len(rates)]]
        next_rate = self.model.predict(next_index)[0]
        return round(next_rate, 4)
