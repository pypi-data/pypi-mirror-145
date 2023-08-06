import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import _check_feature_names_in


class CorrelationThreshold(BaseEstimator, TransformerMixin):
    """Removes columns based on correlation between columns.
    
    Attributes:
        threshold: if higher than threshold, then column will be removed!
    """
    
    
    def __init__(self, threshold = .95, criteria = None):
        """Init CorrelationThreshold class."""
        self.threshold = threshold
        self.criteria = criteria
        self.ls_idx_keeped_cols = []
        
    
    def fit(self, X, y=None):
        """Fit method for train subset.
        
        Args:
            X (array-like): input matrix.
            y (array-like): not needed, exists for compatibility.
        """
        # Work with pandas
        _df = pd.DataFrame(np.array(X), columns = np.arange(X.shape[1]))

        # Correlation matrix ordered
        so = _df.corr().abs().unstack().\
                sort_values(kind="quicksort", ascending = False)

        # Convert to dictionary:
        # - no consider a column with itself 
        # - sort names to avoid duplicates
        # - only consider those pairs of columns with a correlation higher than threshold
        self._d_idx_corr = {tuple(sorted(k)):v for k,v in so.to_dict().items() if 
                                                    ((k[0] != k[1]) & (v >= self.threshold))}

        return self
    
    
    def transform(self, X) -> np.array:
        """Transform method.
        
        Args:
            X (array-like): input matrix.
        """
        
        # Work with pandas
        _df = pd.DataFrame(np.array(X), columns = np.arange(X.shape[1]))
        
        # Initialize columns to be removed
        ls_idx_removed = []

        # Remove that columns with more Nones. Otherwise remove first column
        if self.criteria is None:
            for c1, c2 in self._d_idx_corr.keys():
                ls_idx_removed.append(
                    _df[[c1,c2]].isnull().sum().\
                            sort_values(kind="quicksort", ascending = False).keys()[0]
                )

        # Remove that columns with more Nones, but complete missing values first
        if self.criteria == 'complete':
            for c1, c2 in self._d_idx_corr.keys():
                ls_idx_removed.append(
                    _df[[c1,c2]].isnull().sum().\
                            sort_values(kind="quicksort", ascending = False).keys()[0]
                )
                _df[c1] = _df[c1].fillna(_df[c2])
                _df[c2] = _df[c2].fillna(_df[c1])
        
        self.ls_idx_keeped_cols = [x for x in _df.columns if x not in ls_idx_removed]
        return _df.loc[:, self.ls_idx_keeped_cols].to_numpy()
    
    
    def get_feature_names_out(self, input_features=None) -> list:
        """To get column names after transformation.
        
        Args:
            features_in (array, optional): Dummy Argument for compatibility. 
                Defaults to None.
        
        Returns:
            List of strings with column names"""
        
        
        ls_colnames = _check_feature_names_in(self, input_features)
        return np.array(ls_colnames)[self.ls_idx_keeped_cols]