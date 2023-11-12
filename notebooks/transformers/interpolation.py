from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class InterpolationTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, method="linear", order=None):
        self.method = method
        self.order = order

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame, y=None) -> pd.DataFrame:
        X_copy = X.copy()
        X_copy.interpolate(method=self.method, order=self.order, inplace=True)

        return X_copy
