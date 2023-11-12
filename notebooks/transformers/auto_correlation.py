from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import pacf


class AutocorrelationTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, max_n_lags=3, max_lag=10):
        if 10 < max_n_lags < 1:
            raise ValueError("max_lags should be between 1 and 10")

        self.significant_lags = None
        self.max_n_lags = max_n_lags
        self.max_lag = max_lag

    def fit(self, X: pd.DataFrame, y=None):
        X_copy = X.copy()
        value = X_copy["value"]

        # Calculate the PACF values
        pacf_values = pacf(
            value,
            nlags=self.max_lag,
        )

        # Pick the top lags
        significant_lags = np.argsort(abs(np.array(pacf_values)))[::-1]
        self.significant_lags = significant_lags[1 : self.max_n_lags + 1]

        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_copy = X.copy()
        value = X_copy["value"]

        # Excluding the first lag (autocorrelation = 1) and Lag 0 (constant)
        correlation_features = pd.DataFrame(
            index=X_copy.index,
            columns=[f"lag_{lag}" for lag in self.significant_lags],
        )

        for lag in self.significant_lags:
            correlation_features.loc[:, f"lag_{lag}"] = value.shift(lag)

        # Backfill the NaN values
        correlation_features = correlation_features.bfill()

        return pd.concat([X, correlation_features], axis=1)
