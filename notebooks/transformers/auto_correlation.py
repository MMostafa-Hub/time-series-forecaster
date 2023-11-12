from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import pacf


class AutocorrelationTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, max_n_lags=3):
        if 10 < max_n_lags < 1:
            raise ValueError("max_lags should be between 1 and 10")

        self.significant_lags = None
        self.max_n_lags = max_n_lags
        self.max_lag = None

    def fit(self, X: pd.DataFrame, y=None):
        X_copy = X.copy()
        value = X_copy["value"]

        # Calculate the PACF values
        pacf_values = pacf(
            value,
            nlags=10,
        )

        # Sort the PACF values
        top_pacf_values = list(
            filter(
                lambda pacf_value: abs(pacf_value) > 2 / len(value) ** 0.5, pacf_values
            )
        )

        # Pick the top lags
        significant_lags = np.argsort(abs(np.array(top_pacf_values)))[::-1]
        self.significant_lags = significant_lags[1 : self.max_n_lags + 1]

        # Calculate the max lag
        self.max_lag = max(self.significant_lags)

        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_copy = X.copy()
        value = X_copy["value"]

        # Excluding the first lag (autocorrelation = 1) and Lag 0 (constant)
        correlation_features = pd.DataFrame(
            index=X_copy.index,
            columns=[f"lag_{i}" for i in range(1, self.max_lag)],
        )

        for i, lag in enumerate(self.significant_lags):
            correlation_features.loc[:, f"lag_{i}"] = value.shift(lag)

        # Backfill the NaN values
        correlation_features = correlation_features.bfill()

        return pd.concat([X, correlation_features], axis=1)