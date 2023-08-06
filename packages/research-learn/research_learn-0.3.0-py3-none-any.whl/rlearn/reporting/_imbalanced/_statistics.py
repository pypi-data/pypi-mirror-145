"""
It contains functions to report the results of model
search and experiments.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# Licence: MIT

from collections import Counter
import warnings

from scipy.stats import friedmanchisquare, ttest_rel
from statsmodels.stats.multitest import multipletests
import pandas as pd


def _extract_pvalue(df):
    """Extract the p-value."""
    results = friedmanchisquare(*df.iloc[:, 3:].transpose().values.tolist())
    return results.pvalue


def apply_friedman_test(imbalanced_experiment, alpha=0.05):
    """Apply the Friedman test across datasets for every
    combination of classifiers and metrics.

    Parameters
    ----------
    imbalanced_experiment : object of :class:`rlearn.experiment.ImbalancedClassificationExperiment` class
        The fitted imbalanced experiment object.

    Returns
    -------
    friedman_test : object of :class:`pd.DataFrame` class
        The results of the test as a pandas DataFrame.
    """

    # Calculate ranking results
    ovrs_names = imbalanced_experiment.results_wide_tbl_.columns[3:]

    # Apply test for more than two oversamplers
    if len(ovrs_names) < 3:
        warnings.warn(
            'More than two oversamplers are required apply the Friedman test.'
        )

    # Calculate p-values
    friedman_test = (
        imbalanced_experiment.results_wide_tbl_.groupby(['classifier', 'metric'])
        .apply(_extract_pvalue)
        .reset_index()
        .rename(columns={0: 'p_value'})
    )

    # Compare p-values to significance level
    friedman_test['significance'] = friedman_test['p_value'] < alpha

    return friedman_test


def apply_holms_test(imbalanced_experiment, control_oversampler=None):
    """Use the Holm's method to adjust the p-values of a paired difference
    t-test for every combination of classifiers and metrics using a control
    oversampler.

    Parameters
    ----------
    imbalanced_experiment : object of :class:`rlearn.experiment.ImbalancedClassificationExperiment` class
        The fitted imbalanced experiment object.
    control_oversampler : str or None, default=None
        The name of the control oversampler. The default oversampler is the last one.

    Returns
    -------
    holms_test : object of :class:`pd.DataFrame` class
        The results of the test as a pandas DataFrame.
    """

    # Calculate wide optimal results
    ovrs_names = list(imbalanced_experiment.results_wide_tbl_.columns[3:])

    # Apply test for more than one oversampler
    if len(ovrs_names) < 2:
        warnings.warn('More than one oversampler is required to apply the Holms test.')

    # Use the last if no control oversampler is provided
    if control_oversampler is None:
        control_oversampler = ovrs_names[-1]
    ovrs_names.remove(control_oversampler)

    # Define empty p-values table
    pvalues = pd.DataFrame()

    # Populate p-values table
    for name in ovrs_names:
        pvalues_pair = imbalanced_experiment.results_wide_tbl_.groupby(
            ['classifier', 'metric']
        )[[name, control_oversampler]].apply(
            lambda df: ttest_rel(df[name], df[control_oversampler])[1]
        )
        pvalues_pair = pd.DataFrame(pvalues_pair, columns=[name])
        pvalues = pd.concat([pvalues, pvalues_pair], axis=1)

    # Corrected p-values
    holms_test = pd.DataFrame(
        pvalues.apply(
            lambda col: multipletests(col, method='holm')[1], axis=1
        ).values.tolist(),
        columns=ovrs_names,
    )
    holms_test = holms_test.set_index(pvalues.index).reset_index()

    return holms_test
