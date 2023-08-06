"""
Test the imbalanced module.
"""

import pytest
from sklearn.base import clone
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE, BorderlineSMOTE

from rlearn.experiment import ImbalancedClassificationExperiment

RND_SEED = 23
DATASETS = [
    ('A', make_classification(random_state=RND_SEED, n_features=10, n_samples=50)),
    ('B', make_classification(random_state=RND_SEED + 2, n_features=20, n_samples=50)),
    ('C', make_classification(random_state=RND_SEED + 5, n_features=5, n_samples=50)),
]
EXPERIMENT = ImbalancedClassificationExperiment(
    oversamplers=[
        ('random_over', RandomOverSampler(), {}),
        ('smote', SMOTE(), {'k_neighbors': [2, 3, 4]}),
        ('bsmote', BorderlineSMOTE(), {'k_neighbors': [3, 4, 5]}),
    ],
    classifiers=[
        ('dtc', DecisionTreeClassifier(), {'max_depth': [3, 5]}),
        ('knc', KNeighborsClassifier(), {}),
    ],
    random_state=RND_SEED,
)


@pytest.mark.parametrize(
    'scoring,n_runs', [(None, 2), ('accuracy', 3), (['accuracy', 'recall'], 2)]
)
def test_experiment_initialization(scoring, n_runs):
    """Test the initialization of experiment's parameters."""

    # Clone and fit experiment
    experiment = clone(EXPERIMENT)
    experiment.set_params(scoring=scoring, n_runs=n_runs)
    experiment.fit(DATASETS)

    # Assertions
    if scoring is None:
        assert experiment.scoring_cols_ == ['accuracy']
    elif isinstance(scoring, str):
        assert experiment.scoring_cols_ == [scoring]
    else:
        assert experiment.scoring_cols_ == scoring
    assert experiment.datasets_names_ == ('A', 'B', 'C')
    assert experiment.oversamplers_names_ == ('random_over', 'smote', 'bsmote')
    assert experiment.classifiers_names_ == ('dtc', 'knc')
    assert len(experiment.estimators_) == 6


def test_experiment_results():
    """Test the results."""

    # Clone and fit experiment
    experiment = clone(EXPERIMENT).fit(DATASETS)

    n_ovrs = len(EXPERIMENT.oversamplers)
    n_clfs = len(EXPERIMENT.classifiers)
    assert list(experiment.results_tbl_.columns) == experiment.GROUP_KEYS + [
        'metric',
        'mean_score',
        'std_score',
    ]
    assert len(experiment.results_tbl_) == len(DATASETS) * n_clfs * n_ovrs


def test_experimet_wide_results():
    """Test the wide format of results."""

    # Clone and fit experiment
    experiment = clone(EXPERIMENT).fit(DATASETS)

    ds_names = experiment.results_wide_tbl_.dataset_name.unique()
    clfs_names = experiment.results_wide_tbl_.classifier.unique()
    metric_names = experiment.results_wide_tbl_.metric.unique()
    assert set(ds_names) == set(experiment.datasets_names_)
    assert len(experiment.results_wide_tbl_) == len(ds_names) * len(clfs_names) * len(
        metric_names
    )
