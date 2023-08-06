import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import _check_feature_names_in


class OutlierConversor(BaseEstimator, TransformerMixin):
    """Transformer which converts the outliers to the maximum values of the interquartile range.
    """
    
    def __init__(self, factor=1.5):
        self.factor = factor
        
    def _outlier_detector(self,X):
        """Internal function to calculate quartiles bounds.
        """
        X = pd.Series(X).copy()
        q1 = X.quantile(0.25)
        q3 = X.quantile(0.75)
        iqr = q3 - q1
        self.lower_bound.append(q1 - (self.factor * iqr))
        self.upper_bound.append(q3 + (self.factor * iqr))

    def fit(self,X,y=None):
        """Fit method for train subset.
        
        Args:
            X (array-like): input matrix.
            y (array-like): not needed, exists for compatibility.
        """
        _df = pd.DataFrame(X)
        self.lower_bound = []
        self.upper_bound = []
        _df.apply(self._outlier_detector)
        return self
    
    def transform(self,X) -> np.array:
        """Transform method.
        
        Args:
            X (array-like): input matrix.
        """
        _df = pd.DataFrame(X).copy()
        for i in range(_df.shape[1]):
            x = _df.iloc[:, i].copy()
            x[(x < self.lower_bound[i]) | (x > self.upper_bound[i])] = np.nan
            _df.iloc[:, i] = x
        return _df.to_numpy()
    
    
    def get_feature_names_out(self, input_features=None):
        return _check_feature_names_in(self, input_features)