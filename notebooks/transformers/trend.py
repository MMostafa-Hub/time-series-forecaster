from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np


# Create Trend Transformer class
class TrendTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, window_size=10, degree=3):
        self.window_size = window_size
        self.degree = degree
        self.lr = LinearRegression()
        self.poly = PolynomialFeatures(degree=self.degree)

    def fit(self, X: pd.DataFrame, y=None):
        X_copy = X.copy()

        values = X_copy["value"]
        timestamps = X_copy.index.values.reshape(-1, 1).astype(float)

        # Calculate the trend using the window average
        expanding_mean = values.expanding(self.window_size).mean().bfill().to_numpy()

        # Create the features for the linear regression
        features = self.poly.fit_transform(timestamps)

        # Fit the linear regression
        self.lr.fit(features, expanding_mean.reshape(-1, 1))

        return self

    def transform(self, X: np.ndarray, y=None) -> pd.DataFrame:
        X_copy = X.copy()
        timestamps = X_copy.index.values.reshape(-1, 1).astype(float)

        features = self.poly.fit_transform(timestamps)
        trend = self.lr.predict(features)

        return pd.concat(
            [X, pd.DataFrame(data=trend, index=X.index, columns=["trend"])], axis=1
        )
