from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='csklearn',
    url='https://github.com/danielruneda/csklearn',
    author='Daniel Runeda',
    author_email='danielruneda@gmail.com',
    # Needed to actually package something
    packages=[
        'csklearn', 
        'csklearn.architecture_templates',
        'csklearn.feature_selection',
        'csklearn.metrics',
        'csklearn.model_selection',
        'csklearn.preprocessing',
        'csklearn.reports',
        'csklearn.transformers',
        'csklearn.utils',
        'csklearn.wrappers',
    ],
    scripts=[
        'csklearn/architecture_templates/tabular_nlp.py',
        'csklearn/feature_selection/correlation_threshold.py',
        'csklearn/metrics/get_scores.py',
        'csklearn/metrics/root_mean_squared_error.py',
        'csklearn/model_selection/CustomStratifiedKFold.py',
        'csklearn/preprocessing/as_type.py',
        'csklearn/preprocessing/OutlierConversor.py',
        'csklearn/preprocessing/TextPreprocessing.py',
        'csklearn/reports/classifier_plots.py',
        'csklearn/reports/get_classification_report.py',
        'csklearn/reports/get_mean_predict_proba.py',
        'csklearn/reports/permutation_importances.py',
        'csklearn/reports/perturbate_and_validate.py',
        'csklearn/reports/plot_model_importances.py',
        'csklearn/reports/plot_pca_variability.py',
        'csklearn/reports/regressor_plots.py',
        'csklearn/transformers/GradientBoostingFeatureGenerator.py',
        'csklearn/transformers/ModelTransformer.py',
        'csklearn/transformers/VariableSelection.py',
        'csklearn/utils/check_params.py',
        'csklearn/utils/get_params_names.py',
        'csklearn/wrappers/wrapper_ce_feature_names_out.py',
        'csklearn/wrappers/wrapper_feature_names_out.py'
        ],
    # Needed for dependencies
    install_requires=[
        'numpy',
        'pandas',
        'matplotlib',
        'scikit-learn'
        # 'eli5',
        ],
    # *strongly* suggested for sharing
    version='0.0.24',
    # The license can be anything you like
    # license='MIT',
    # description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
    python_requires='>=3.6',
    # The package can not run directly from zip file
    zip_safe=False
)