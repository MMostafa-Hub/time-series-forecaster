from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np


class SeasonalityFeaturesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, top=5):
        self.top = top
        self.top_freq: None

    def fit(self, X: pd.DataFrame, y=None):
        if X.isna().sum().value > 0:
            raise ValueError("The dataset contains NaN values")

        if X.shape[1] != 1:
            raise ValueError("The dataset should contain only one column")

        # Copy the value column from the dataset
        X_copy = X.copy().value

        fft_result = np.fft.fft(X_copy)
        # Calculate only positive power spectral density and frequencies
        # Exclude the first value (0 Hz)
        psd = (np.abs(fft_result) ** 2)[: len(X_copy) // 2][1:]
        freq = np.fft.fftfreq(len(X_copy), 1)[: len(X_copy) // 2][1:]

        # Pick the top frequencies
        top_freq_indices = np.argsort(psd, axis=0)[::-1][: self.top]
        self.top_freq = freq[top_freq_indices]

        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        if X.isna().sum().value > 0:
            raise ValueError("The dataset contains NaN values")

        if X.shape[1] != 1:
            raise ValueError("The dataset should contain only one column")

        X_copy = X.copy().index.values.astype(float)

        # Calculate the seasonality features
        seasonality_features = pd.DataFrame(
            index=X.index,
            columns=[f"seasonality_sin_{i}" for i in range(self.top)]
            + [f"seasonality_cos_{i}" for i in range(self.top)],
            dtype=float,
        )
        for i, freq in enumerate(self.top_freq):
            seasonality_features.loc[:, f"seasonality_sin_{i}"] = np.sin(
                2 * np.pi * freq * X_copy
            )
            seasonality_features.loc[:, f"seasonality_cos_{i}"] = np.cos(
                2 * np.pi * freq * X_copy
            )

        # Add the seasonality features to the dataset
        return pd.concat([X, seasonality_features], axis=1)
