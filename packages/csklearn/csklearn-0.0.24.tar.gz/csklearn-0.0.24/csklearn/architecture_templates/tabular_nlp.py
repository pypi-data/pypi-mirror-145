# Machine Learning Modules
from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.pipeline import *
from sklearn.preprocessing import *

# User defined functions
from csklearn.preprocessing.as_type import as_str
from csklearn.preprocessing.TextPreprocessing import *
from csklearn.transformers.VariableSelection import VariableSelection
from csklearn.wrappers.wrapper_feature_names_out import wSimpleImputer

# Text preprocessing
txt_tf = Pipeline(steps=[
                    ('varsel', VariableSelection()),
                    ('tostr', as_str()),
                    ('na', wSimpleImputer(strategy='constant', fill_value='null')),
                    ('tc', TextCleaning()),
                    ('tte', TextEncoding()),
                    ('ohew', OneHotEncodingWords()),
                ])