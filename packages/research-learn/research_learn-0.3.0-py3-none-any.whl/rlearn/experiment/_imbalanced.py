"""
It supports the design and execution of
machine learning experiments on imbalanced
classification data.
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# Licence: MIT

from functools import cached_property
from itertools import product

from joblib import Parallel, delayed
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.metrics import SCORERS
from sklearn.utils.validation import check_is_fitted

from ..utils import check_datasets, check_oversamplers_classifiers, check_random_states
from ..model_selection import ModelSearchCV


class ImbalancedClassificationExperiment(BaseEstimator):
    """Define a classification experiment on multiple imbalanced datasets.

    ImbalancedClassificationExperiment implements a "fit" method tha applies nested cross-validation
    to a collection of oversamplers, classifiers and their parameters.

    Read more in the :ref:`User Guide <user_guide>`.

    Parameters
    ----------
    oversamplers : list of (string, oversampler, param_grid) tuples
        Each oversampler is assumed to implement the imbalanced-learn
        oversampler interface.

    classifiers : list of (string, classifier, param_grid) tuples
        Each classifier is assumed to implement the scikit-learn
        estimator interface.

    scoring : string, callable, list/tuple, dict or None, optional (default=None)
        A single string or a callable to evaluate the predictions on the
        test sets and report the results.

        For evaluating multiple metrics, either give a list of (unique) strings
        or a dict with names as keys and callables as values.

        NOTE that when using custom scorers, each scorer should return a single
        value. Metric functions returning a list/array of values can be wrapped
        into multiple scorers that return one value each.

        If ``None``, a default scorer is used.

    n_splits : int, default=5
        Number of folds for StratifiedKFold cross-validation. Must be at least 2.

    n_runs : int, default=1
        Number of experiment runs. Must be at least 1.

    random_state : int, RandomState instance, default=None
        Control the randomization of the algorithm.

        - If int, ``random_state`` is the seed used by the random number generator.

        - If ``RandomState`` instance, random_state is the random number generator.

        - If ``None``, the random number generator is the ``RandomState`` instance used by ``np.random``.

    n_jobs : int or None, default=None
        Number of jobs to run in parallel.

        - When ``None`` means 1 unless in a :obj:`joblib.parallel_backend` context.

        - When ``-1`` means using all processors.

    verbose : int, default=0
        Controls the verbosity: the higher, the more messages.

    Attributes
    ----------
    result_tbl_ : object of :class:`pandas.DataFrame` class
        A dataframe that contains the results of the experiment. Each column
        includes the dataset name, the name of the oversampler and classifier,
        the metric and the mean/standard deviation score across runs.
    result_wide_tbl_ : object of :class:`pandas.DataFrame` class
        A dataframe that contains the results of the experiment in a wide format.
        It also contains the ranking of the oversampler for each dataset.

    Examples
    --------
    >>> from sklearn.datasets import load_breast_cancer, load_iris
    >>> from sklearn.tree import DecisionTreeClassifier
    >>> from imblearn.over_sampling import RandomOverSampler, SMOTE
    >>> from rlearn.experiment import ImbalancedClassificationExperiment
    >>> datasets = [
    ...     ('breast_cancer', load_breast_cancer(return_X_y=True)),
    ...     ('iris', load_iris(return_X_y=True))
    ... ]
    >>> experiment = ImbalancedClassificationExperiment(
    ...     oversamplers=[('random_over', RandomOverSampler(), {}), ('smote', SMOTE(), {'k_neighbors': [3, 5]} )],
    ...     classifiers = [('tree', DecisionTreeClassifier(), {'max_depth': [3,5, 8]})],
    ...     random_state=12
    ... )
    >>> experiment.fit(datasets)
    ImbalancedClassificationExperiment(classifiers=[('tree',...
    >>> experiment.results_tbl_
        dataset_name  oversampler classifier    metric  mean_score  std_score
    0  breast_cancer  random_over       tree  accuracy    0.926168   0.009979
    1  breast_cancer        smote       tree  accuracy    0.942804   0.003777
    2           iris  random_over       tree  accuracy    0.943333   0.004714
    3           iris        smote       tree  accuracy    0.943333   0.004714
    >>> experiment.results_wide_tbl_
        dataset_name classifier    metric  random_over_score  smote_score  random_over_rank  smote_rank
    0  breast_cancer       tree  accuracy           0.926168     0.942804               2.0         1.0
    1           iris       tree  accuracy           0.943333     0.943333               1.5         1.5
    """

    GROUP_KEYS = ['dataset_name', 'oversampler', 'classifier']

    def __init__(
        self,
        oversamplers,
        classifiers,
        scoring=None,
        n_splits=5,
        n_runs=2,
        random_state=None,
        n_jobs=-1,
        verbose=0,
    ):
        self.oversamplers = oversamplers
        self.classifiers = classifiers
        self.scoring = scoring
        self.n_splits = n_splits
        self.n_runs = n_runs
        self.random_state = random_state
        self.n_jobs = n_jobs
        self.verbose = verbose

    def _check_estimators(self):
        """Check the estimators."""
        estimators, param_grids = check_oversamplers_classifiers(
            self.oversamplers, self.classifiers
        )
        self.estimators_ = []
        for name, estimator in estimators:
            selected_param_grids = []
            for param_grid in param_grids:
                selected_param_grid = {}
                if param_grid['est_name'][0] == name:
                    for param_name, vals in param_grid.items():
                        if param_name != 'est_name':
                            selected_param_grid[
                                param_name.replace(f'{name}__', '')
                            ] = vals
                    selected_param_grids.append(selected_param_grid)
            self.estimators_.append(
                (name, GridSearchCV(estimator, selected_param_grids))
            )
        return self

    def _check_mscv(self):
        self.mscv_ = ModelSearchCV(
            self.estimators_,
            {},
            scoring=self.scoring,
            refit=False,
            cv=StratifiedKFold(
                n_splits=self.n_splits, shuffle=True, random_state=self.random_state
            ),
            return_train_score=False,
            n_jobs=self.n_jobs,
            verbose=self.verbose,
        )
        return self

    def _check_cols(self, datasets):

        # Extract names
        self.oversamplers_names_, *_ = zip(*self.oversamplers)
        self.classifiers_names_, *_ = zip(*self.classifiers)
        self.datasets_names_, _ = zip(*datasets)

        # Extract scoring columns
        if isinstance(self.scoring, list):
            self.scoring_cols_ = self.scoring
        elif isinstance(self.scoring, str):
            self.scoring_cols_ = [self.scoring]
        else:
            self.scoring_cols_ = (
                ['accuracy']
                if self.mscv_.estimator._estimator_type == 'classifier'
                else ['r2']
            )
        return self

    def _check_random_states_mapping(self):
        self.random_states_mapping_ = {
            run_id: random_state
            for run_id, random_state in enumerate(
                check_random_states(self.random_state, self.n_runs)
            )
        }
        return self

    def _set_random_state(self, run_id):
        random_state = self.random_states_mapping_[run_id]
        for _, estimator in self.mscv_.get_params()['estimators']:
            for param_name in estimator.get_params().keys():
                if param_name.endswith('__random_state'):
                    estimator.set_params(**{param_name: random_state})
        return self

    def _fit(self, run_id, dataset_name, X, y):

        # Fit model search
        self._set_random_state(run_id).mscv_.fit(X, y)

        # Get results
        result = pd.DataFrame(self.mscv_.cv_results_)
        result = result.assign(run_id=run_id, dataset_name=dataset_name)
        scoring_cols = [col for col in result.columns.tolist() if 'mean_test' in col]
        result.rename(columns=dict(zip(scoring_cols, self.scoring_cols_)), inplace=True)
        result = result.loc[
            :, ['run_id', 'dataset_name', 'param_est_name'] + self.scoring_cols_
        ]
        select_name = lambda names, model: [
            name for name in names if set(name.split('_')).issubset(model.split('_'))
        ][0]
        result.loc[:, 'param_est_name'] = result.loc[:, 'param_est_name'].apply(
            lambda model: [
                select_name(self.oversamplers_names_, model),
                select_name(self.classifiers_names_, model),
            ]
        )
        result[['oversampler', 'classifier']] = pd.DataFrame(
            result['param_est_name'].values.tolist()
        )
        result.drop(columns='param_est_name', inplace=True)
        result = result.melt(
            id_vars=['run_id'] + self.GROUP_KEYS,
            value_vars=self.scoring_cols_,
            var_name='metric',
            value_name='score',
        )

        return result

    def fit(self, datasets):
        """Fit the experiment to the datasets.

        Parameters
        ----------
        datasets : list of (name, (X, y)) tuples
            The datasets that are used to fit the oversamplers
            and classifiers of the experiment.

        Returns
        -------
        self : object
            Return the instance itself.
        """

        # Checks
        datasets = check_datasets(datasets)
        self._check_estimators()._check_mscv()._check_cols(
            datasets
        )._check_random_states_mapping()

        # Get results
        results = Parallel(n_jobs=self.n_jobs)(
            delayed(self._fit)(run_id, dataset_name, X, y)
            for run_id, (dataset_name, (X, y)) in product(range(self.n_runs), datasets)
        )
        results = pd.concat(results, ignore_index=True)

        # Calculate results
        self.results_tbl_ = (
            results.groupby(self.GROUP_KEYS + ['metric'])
            .score.agg(mean_score='mean', std_score='std')
            .reset_index()
        )

        return self

    @staticmethod
    def _return_row_ranking(row, sign):
        """Returns the ranking of values. In case of tie, each ranking value
        is replaced with its group average."""

        # Calculate ranking
        ranking = (sign * row).argsort().argsort().astype(float)

        # Break the tie
        groups = np.unique(row, return_inverse=True)[1]
        for group_label in np.unique(groups):
            indices = groups == group_label
            ranking[indices] = ranking[indices].mean()

        return ranking.size - ranking

    @cached_property
    def results_wide_tbl_(self):
        check_is_fitted(self, 'results_tbl_')
        scores = self.results_tbl_.pivot_table(
            index=['dataset_name', 'classifier', 'metric'],
            columns=['oversampler'],
            values='mean_score',
        ).reset_index()
        scores.rename_axis(None, axis=1, inplace=True)
        ranks = scores.apply(
            lambda row: self._return_row_ranking(
                row[3:], SCORERS[row[2].replace(' ', '_').lower()]._sign
            ),
            axis=1,
        )
        col_mapping = lambda cols, suffix: dict(
            zip(cols, [f'{col}_{suffix}' for col in cols])
        )
        scores.rename(columns=col_mapping(scores.columns[3:], 'score'), inplace=True)
        ranks.rename(columns=col_mapping(ranks.columns, 'rank'), inplace=True)
        tbl = pd.concat([scores, ranks], axis=1)
        return tbl
