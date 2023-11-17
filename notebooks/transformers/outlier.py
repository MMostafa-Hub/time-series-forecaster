from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np


class OutlierTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.X_mean = None
        self.X_std = None

    def fit(self, X, y=None):
        """Calculate the z-score for each column in the DataFrame"""
        X_copy = X.copy().to_numpy()
        self.X_mean = np.mean(X_copy)
        self.X_std = np.std(X_copy)

        return self

    def __zscore(self, X):
        X = np.nan_to_num(X, copy=True, nan=0)  # Convert the NaN values to 0

        return (X - self.X_mean) / np.std(self.X_std)

    def transform(self, X: pd.DataFrame, y=None):
        """
        remove the rows with z-score > threshold
        """
        X_copy = X.copy()

        z_scores = self.__zscore(X_copy.value)
        outliers = np.abs(z_scores) > self.threshold
        X_copy[outliers] = np.nan

        return pd.DataFrame(X_copy, columns=X.columns, index=X.index)
