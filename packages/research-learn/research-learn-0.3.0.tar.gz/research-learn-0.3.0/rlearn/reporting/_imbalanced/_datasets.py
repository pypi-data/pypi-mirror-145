"""
It contains functions to report the results of model
search and experiments.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# Licence: MIT

from collections import Counter

import pandas as pd

from ...utils import check_datasets


def summarize_imbalanced_binary_datasets(datasets):
    """Create a summary of imbalanced datasets.

    Parameters
    ----------
    datasets : list of (name, (X, y)) tuples
        The datasets to describe their properties.

    Returns
    -------
    datasets_summery : object of :class:`pd.DataFrame` class
        A summary of the datasets properties.
    """

    # Check datasets format
    check_datasets(datasets)

    # Define summary table columns
    summary_columns = [
        "dataset_name",
        "features",
        "instances",
        "minority_instances",
        "majority_instances",
        "imbalance_ratio",
    ]

    # Define empty summary table
    datasets_summary = []

    # Populate summary table
    for dataset_name, (X, y) in datasets:
        n_instances = Counter(y).values()
        n_minority_instances, n_majority_instances = min(n_instances), max(n_instances)
        values = [
            dataset_name,
            X.shape[1],
            len(X),
            n_minority_instances,
            n_majority_instances,
            round(n_majority_instances / n_minority_instances, 2),
        ]
        datasets_summary.append(values)
    datasets_summary = pd.DataFrame(datasets_summary, columns=summary_columns)

    # Cast to integer columns
    datasets_summary[summary_columns[1:-1]] = datasets_summary[
        summary_columns[1:-1]
    ].astype(int)

    # Sort datasets summary
    datasets_summary = datasets_summary.sort_values('imbalance_ratio').reset_index(
        drop=True
    )

    return datasets_summary
