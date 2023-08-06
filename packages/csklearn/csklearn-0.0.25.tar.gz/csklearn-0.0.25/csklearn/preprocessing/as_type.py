import scipy
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

    def __init__(self, flatten = False):
        """_summary_

        Args:
            flatten (bool, optional): wheter flatten or not. If is a sparse csr matrix, 
                then not applies. Defaults to False.
        """
        self.flatten = flatten

    def fit(self, X, y=None, **kwargs):
        """Dummy fit function that does nothing particular."""
        return self

    def transform(self, X, y=None, **kwargs):
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
        elif self.flatten:
            return X.values.flatten()
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

    def transform(self, X, y=None, **kwargs):
        """Convert input column X as string type

        Args:
            X (array-like): array-like of shape (n_samples, n_features).
            y (array-like): array-like of shape (n_samples, ). 
                Do nothing. Defaults to None.

        Returns:
            [type]: [description]
        """
        return X.values.flatten()

    def get_feature_names_out(self, input_features=None):
        return _check_feature_names_in(self, input_features)