from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np


class OutlierTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.training_z_scores = None

    def fit(self, X, y=None):
        """Calculate the z-score for each column in the DataFrame"""
        X_copy = X.copy().to_numpy()
        column = X_copy[:, 0]
        z_scores = self.__zscore(column)

        self.training_z_scores = z_scores
        return self

    def __zscore(self, X):
        X = np.nan_to_num(X, copy=True, nan=0)  # Convert the NaN values to 0
        return (X - np.mean(X)) / np.std(X)

    def transform(self, X: pd.DataFrame, y=None):
        """
        remove the rows with z-score > threshold
        """
        X_copy = X.copy().to_numpy()

        outliers = np.abs(self.training_z_scores) > self.threshold
        X_copy[outliers] = np.nan

        return pd.DataFrame(X_copy, columns=X.columns, index=X.index)
