"""
Test the datasets module.
"""

import pandas as pd
from sklearn.datasets import make_classification
from rlearn.reporting import summarize_imbalanced_binary_datasets

DATASETS = [
    ('A', make_classification(weights=[0.90, 0.10], n_samples=300, random_state=0)),
    ('B', make_classification(weights=[0.80, 0.20], n_samples=200, random_state=1)),
    ('C', make_classification(weights=[0.60, 0.40], n_samples=100, random_state=2)),
]


def test_imbalanced_binary_datasets_summary():
    """Test the imbalanced dataset's summary."""
    datasets_summary = summarize_imbalanced_binary_datasets(DATASETS)
    expected_datasets_summary = pd.DataFrame(
        {
            'dataset_name': ['C', 'B', 'A'],
            'features': [20, 20, 20],
            'instances': [100, 200, 300],
            'minority_instances': [40, 41, 32],
            'majority_instances': [60, 159, 268],
            'imbalance_ratio': [1.5, 3.88, 8.38],
        }
    )
    pd.testing.assert_frame_equal(
        datasets_summary, expected_datasets_summary, check_dtype=False
    )
