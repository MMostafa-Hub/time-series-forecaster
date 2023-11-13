from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class TrendTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, window_size=5):
        self.window_size = window_size

    def fit(self, X: pd.DataFrame, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_copy = X.copy()
        values = X_copy["value"]

        # Calculate the trend using the window average
        expanding_mean = values.expanding(self.window_size).mean().bfill().to_numpy()

        return pd.concat(
            [
                X,
                pd.DataFrame(
                    data=expanding_mean, index=X_copy.index, columns=["trend"]
                ),
            ],
            axis=1,
        )
