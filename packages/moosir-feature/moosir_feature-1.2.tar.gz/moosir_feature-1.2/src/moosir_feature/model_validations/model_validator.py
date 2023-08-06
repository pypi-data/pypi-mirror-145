import numpy as np
import pandas as pd
from sklearn.utils import shuffle
from sklearn.model_selection import TimeSeriesSplit
from pandas.testing import assert_index_equal

TRAIN_FEATURE_KEY = "train_feature"
TRAIN_TARGET_KEY = "train_target"
TEST_FEATURE_KEY = "test_feature"
TEST_TARGET_KEY = "test_target"


def shuffle_df(data: pd.DataFrame, target_col: str, rand_state: int = None):
    targets = data[[target_col]]
    features = data[data.columns[~data.columns.isin([target_col])]]

    assert len(features.columns) > 1, "no column left for feature"

    if rand_state is None:
        rand_state = np.random.randint(1000)

    features_shuf_ind, targets_shuf_ind = shuffle(features.index, targets.index, random_state=rand_state)

    features_shuf = features.loc[features_shuf_ind]
    targets_shuf = targets.loc[targets_shuf_ind]

    all_shuf = data.loc[features_shuf_ind]

    return features_shuf, targets_shuf, all_shuf, rand_state


def create_timeseries_cv(train_n, test_n, sample_n):
    # see the sklearn code for invalid split number
    split_n = int((sample_n + 1) / test_n) - 1
    print(split_n)
    assert split_n > 1, "split is 1"

    tscv = TimeSeriesSplit(max_train_size=train_n, test_size=test_n, n_splits=split_n)
    return tscv


class CustomTsCv:
    """
      in addition to sklearn time series can shuffle train data in blocks
    """
    def __init__(self, train_n: int, test_n: int, sample_n: int, train_shuffle_block_size: int = None):
        split_n = int((sample_n + 1) / test_n) - 1
        print(split_n)
        assert split_n > 1, "split is 1"

        if train_shuffle_block_size is not None:
            assert train_n % train_shuffle_block_size == 0, "train data is not devidable in shuffle block size"

        self.train_shuffle_block_size = train_shuffle_block_size
        self.tscv = TimeSeriesSplit(max_train_size=train_n, test_size=test_n, n_splits=split_n)

    def split(self, X, y, groups=None):
        for tr, ts in self.tscv.split(X=X, y=y, groups=groups):
            final_tr = tr
            final_ts = ts
            if self.train_shuffle_block_size is not None:
                np.random.shuffle(final_tr.reshape((-1, self.train_shuffle_block_size)))

            yield final_tr, final_ts

    def get_n_splits(self, X, y, groups=None):
        return self.tscv.n_splits


def cv_ts_df(features: pd.DataFrame,
             targets: pd.DataFrame,
             train_n: int,
             test_n: int,
             shuffle_in_every_train_wind: bool = True,
             verbose: bool = False):
    """
    - creating moving windows for cross validation based on train_n and test_n
    - it also can shuffle data in train/test dataset (for better training)
    """

    features_inds = features.index
    targets_inds = targets.index

    assert train_n + test_n < len(features), "window cant be smaller than data"
    assert len(features) == len(targets), "features and targets must have the same length"
    assert_index_equal(features_inds, targets_inds, "targets and features have mismatching indexes")

    sample_n = len(targets)

    fold_results = {TRAIN_FEATURE_KEY: [],
                    TRAIN_TARGET_KEY: [],
                    TEST_FEATURE_KEY: [],
                    TEST_TARGET_KEY: []
                    }
    tscv = create_timeseries_cv(train_n=train_n, test_n=test_n, sample_n=sample_n)
    for train_index, test_index in tscv.split(features_inds):

        if shuffle_in_every_train_wind:
            train_ind_shuf = shuffle(train_index)
            test_ind_shuf = shuffle(test_index)
        else:
            train_ind_shuf = train_index
            test_ind_shuf = test_index

        if verbose:
            print("TRAIN:", train_index, "TEST:", test_index)
            print("TRAIN SHUF:", train_ind_shuf, "TEST SHUF:", test_ind_shuf)
        X_train, X_test = features.loc[train_ind_shuf], features.loc[test_ind_shuf]
        y_train, y_test = targets.loc[train_ind_shuf], targets.loc[test_ind_shuf]

        fold_results[TRAIN_FEATURE_KEY].append(X_train)
        fold_results[TRAIN_TARGET_KEY].append(y_train)
        fold_results[TEST_FEATURE_KEY].append(X_test)
        fold_results[TEST_TARGET_KEY].append(y_test)

    return fold_results


def calculate_confidence_interval(statistics: pd.DataFrame,
                                  alpha: float = 5.0,
                                  ignore_small_instances: bool = False) -> pd.DataFrame:
    """
    to calculate statistical intervals based on trials
    :param statistics: any estimations coming from running trials (e.g. accuracy, error, ...).
        - dataframe, columns: statistics, row: trials (samples)
    :param alpha: p-value
    :param ignore_small_instances: for too small values, this method cant work, if True, the answer might not be reliable
    :return: dataframe: columns: lower/higher ci, index: statistic name from input statistics
    """
    if not ignore_small_instances:
        assert len(statistics) < 100, "number of trials is too low to build any confidence level"

    # calculate lower percentile (e.g. 2.5)
    lower_p = alpha / 2.0
    # calculate upper percentile (e.g. 97.5)
    upper_p = (100 - alpha) + (alpha / 2.0)

    cis = statistics.quantile([lower_p / 100.0, upper_p / 100.0]).transpose()
    cis.columns = [f"Lower_{lower_p}", f"Upper_{upper_p}"]
    return cis


class CvTsDfUtil:
    @staticmethod
    def get_split_len(fold_result: dict):
        return len(fold_result[TEST_FEATURE_KEY])

    @staticmethod
    def get_train(fold_result: dict, ind: int):
        return fold_result[TRAIN_FEATURE_KEY][ind], fold_result[TRAIN_TARGET_KEY][ind]

    @staticmethod
    def get_test(fold_result: dict, ind: int):
        return fold_result[TEST_FEATURE_KEY][ind], fold_result[TEST_TARGET_KEY][ind]
