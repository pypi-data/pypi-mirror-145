import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_index_equal, assert_extension_array_equal

from moosir_feature.model_validations.model_validator import *


@pytest.fixture
def ohlc_prices():
    return pd.DataFrame(data=np.random.rand(10, 4), columns=["Open", "High", "Low", "Close"])


@pytest.mark.skip()
def test_shuffle_df():
    # arrange
    sample_n = 10
    feature_n = 3
    feature_cols = [f"f_{i}" for i in range(feature_n)]
    target_col = "target"

    features = pd.DataFrame(data=np.random.rand(sample_n, feature_n),
                            index=pd.date_range("2020/01/01", periods=sample_n),
                            columns=feature_cols)
    targets = pd.DataFrame(data=np.random.rand(sample_n, 1),
                           index=pd.date_range("2020/01/01", periods=sample_n),
                           columns=[target_col]
                           )

    data = pd.concat([features, targets], axis=1)

    # act
    features_shuf, targets_shuf, all_shuf, rand_state = shuffle_df(data=data, target_col=target_col)

    # assert
    assert_frame_equal(features_shuf.sort_index().reset_index(drop=True),
                       features.sort_index().reset_index(drop=True),
                       check_index_type=False)

    assert_frame_equal(targets_shuf.sort_index().reset_index(drop=True),
                       targets.sort_index().reset_index(drop=True),
                       check_index_type=False)

    assert_frame_equal(all_shuf.sort_index().reset_index(drop=True),
                       data.sort_index().reset_index(drop=True),
                       check_index_type=False)


@pytest.mark.skip()
def test_cv_ts_df():
    # arrange
    sample_n = 10
    feature_n = 1

    feature_cols = [f"f_{i}" for i in range(feature_n)]
    target_col = "target"
    features = pd.DataFrame(data=np.arange(0, sample_n * feature_n).reshape(sample_n, -1), columns=feature_cols)
    targets = pd.DataFrame(data=np.arange(0, sample_n * 1).reshape(sample_n, -1), columns=[target_col])

    train_n = 4
    test_n = 2

    # act
    fold_results = cv_ts_df(features=features,
                            targets=targets,
                            test_n=test_n,
                            train_n=train_n,
                            verbose=True)

    # assert
    assert len(fold_results[TRAIN_TARGET_KEY]) == 4

    for i in range(CvTsDfUtil.get_split_len(fold_result=fold_results)):
        train_feature_split, train_target_split = CvTsDfUtil.get_train(fold_result=fold_results, ind=i)
        test_feature_split, test_target_split = CvTsDfUtil.get_test(fold_result=fold_results, ind=i)

        assert len(test_feature_split) == test_n
        assert len(test_target_split) == test_n
        assert len(train_feature_split) <= train_n
        assert len(train_target_split) <= train_n

        assert_index_equal(train_target_split.index, train_feature_split.index)
        assert_index_equal(test_target_split.index, test_feature_split.index)

    # todo: more asserts


# @pytest.mark.skip()
def test_calculate_confidence_interval():
    # arrange
    sample_n = 10
    statistics_n = 2

    statistics_cols = [f"stat_{i}" for i in range(statistics_n)]
    statistics = pd.DataFrame(data=np.arange(0, sample_n * statistics_n).reshape(sample_n, -1),
                              columns=statistics_cols)

    # act
    ci_results = calculate_confidence_interval(statistics=statistics, ignore_small_instances=True)

    # assert
    expected = pd.DataFrame(data={"Lower_2.5": [0.45, 1.45], "Upper_97.5": [17.55, 18.55]}, index=["stat_0", "stat_1"])
    assert_frame_equal(expected, ci_results)

