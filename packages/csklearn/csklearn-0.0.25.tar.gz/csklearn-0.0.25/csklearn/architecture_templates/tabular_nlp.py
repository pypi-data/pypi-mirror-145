# Machine Learning Modules
from sklearn.ensemble import *
from sklearn.linear_model import *
from sklearn.pipeline import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

# User defined functions
from csklearn.preprocessing.as_type import *
from csklearn.preprocessing.TextPreprocessing import *
from csklearn.transformers.VariableSelection import VariableSelection
from csklearn.wrappers.wrapper_feature_names_out import wSimpleImputer

# Text preprocessing based on text encoding
def txt_encoding_tf():
    return(
        Pipeline(steps=[
                    ('varsel', VariableSelection()),
                    ('tostr', to_str()),
                    ('na', wSimpleImputer(strategy='constant',
                                            fill_value='null')),
                    ('tc', TextCleaning()),
                    ('tte', TextEncoding()),
                    ('ohew', OneHotEncodingWords()),
                ])
    )


# Text preprocessing based on tfidf
def txt_tfidf_tf():
    return(
        Pipeline(steps=[
                    ('varsel', VariableSelection()),
                    ('tostr', to_str()),
                    ('na', wSimpleImputer(strategy='constant',
                                            fill_value='null')),
                    ('to_np', to_np(flatten = True)), # To use CountVectorizer we need it
                    
                    ("vect", CountVectorizer(analyzer='word')),
                    ("tfidf", TfidfTransformer()),
                ])
    )

