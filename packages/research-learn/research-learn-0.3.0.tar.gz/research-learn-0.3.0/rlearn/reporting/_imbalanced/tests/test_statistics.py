"""
Test the statistics module.
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import make_classification
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN

from rlearn.experiment import ImbalancedClassificationExperiment
from rlearn.reporting import apply_friedman_test, apply_holms_test

OVERSAMPLERS = [
    ('random', RandomOverSampler(), {}),
    ('smote', SMOTE(), {'k_neighbors': [2, 3]}),
    ('adasyn', ADASYN(), {'n_neighbors': [2, 3, 4]}),
]
CLASSIFIERS = [
    ('knn', KNeighborsClassifier(), {}),
    ('dtc', DecisionTreeClassifier(), {'max_depth': [3, 5]}),
]
DATASETS = [
    ('A', make_classification(weights=[0.90, 0.10], n_samples=200, random_state=0)),
    ('B', make_classification(weights=[0.80, 0.20], n_samples=200, random_state=1)),
    ('C', make_classification(weights=[0.60, 0.40], n_samples=200, random_state=2)),
]
EXPERIMENT = ImbalancedClassificationExperiment(
    OVERSAMPLERS, CLASSIFIERS, scoring=None, n_splits=3, n_runs=3, random_state=0
).fit(DATASETS)


def test_friedman_test():
    """Test the results of friedman test."""
    friedman_test = apply_friedman_test(EXPERIMENT, alpha=0.05)
    assert set(friedman_test.classifier.unique()) == set(EXPERIMENT.classifiers_names_)
    assert len(friedman_test) == len(CLASSIFIERS)


def test_holms_test():
    """Test the results of holms test."""
    holms_test = apply_holms_test(EXPERIMENT, control_oversampler=None)
    assert set(holms_test.classifier.unique()) == set(EXPERIMENT.classifiers_names_)
    assert len(holms_test) == len(CLASSIFIERS)
