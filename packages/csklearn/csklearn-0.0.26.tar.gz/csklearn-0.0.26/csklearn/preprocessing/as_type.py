import scipy
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import _check_feature_names_in



class to_str(BaseEstimator, TransformerMixin):
    """
    Transform X into string.
    """

    def fit(self, X, y=None, **kwargs):
        """Dummy fit function that does nothing particular."""
        return self

    def transform(self, X, **kwargs):
        """Convert input column X as string type

        Args:
            X ([type]): [description]

        Returns:
            [type]: [description]
        """
        return X.astype(str)
    
    def get_feature_names_out(self, input_features=None):
        return _check_feature_names_in(self, input_features)


class to_np(BaseEstimator, TransformerMixin):
    """
    Transform X to numpy array if it is sparse csr.
    """

    def fit(self, X, y=None, **kwargs):
        """Dummy fit function that does nothing particular."""
        return self

    def transform(self, X, **kwargs):
        """Convert input column X as string type

        Args:
            X (array-like): array-like of shape (n_samples, n_features).
            y (array-like): array-like of shape (n_samples, ). 
                Do nothing. Defaults to None.

        Returns:
            [type]: [description]
        """
        if isinstance(X, scipy.sparse.csr.csr_matrix):
            return X.toarray()
        else:
            return X.values

    def get_feature_names_out(self, input_features=None):
        return _check_feature_names_in(self, input_features)


class to_np_flatten(BaseEstimator, TransformerMixin):
    """
    Transform X to numpy array if it is sparse csr.
    """

    def fit(self, X, y=None, **kwargs):
        """Dummy fit function that does nothing particular."""
        return self

    def transform(self, X, **kwargs):
        """Convert input column X as string type

        Args:
            X (array-like): array-like of shape (n_samples, n_features).

        Returns:
            [type]: [description]
        """
        X = np.array(X)
        return X.flatten()


    def get_feature_names_out(self, input_features=None):
        return _check_feature_names_in(self, input_features)