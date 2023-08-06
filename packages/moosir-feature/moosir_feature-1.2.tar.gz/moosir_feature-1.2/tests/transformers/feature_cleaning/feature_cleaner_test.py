import numpy as np
import pandas as pd

from moosir_feature.transformers.feature_cleaning.feature_cleaner import *

import pytest


#
def test_normalize_should_scale_cols_separately():
    # arrange
    n_samples = 15
    min_value_f1 = -10
    max_value_f1 = -5

    min_value_f2 = 60000
    max_value_f2 = 70000

    # data = {
    #     "feature_1": np.arange(start=min_value_f1, stop=max_value_f1),
    #     "feature_2": np.arange(start=min_value_f2, stop=max_value_f2)
    # }

    data = {
        "feature_1": np.random.randint(low=min_value_f1, high=max_value_f1, size=n_samples),
        "feature_2": np.random.randint(low=min_value_f2, high=max_value_f2, size=n_samples)
    }

    data = pd.DataFrame(data=data)

    # act
    transformed, scaler = normalize(data=data)

    # assert
    dec_points = 5
    assert round(transformed["feature_1"].max(), dec_points) == 1
    assert round(transformed["feature_1"].min(), dec_points) == 0

    assert round(transformed["feature_2"].max(), dec_points) == 1
    assert round(transformed["feature_2"].min(), dec_points) == 0

# def test_normalize_on_none_numeric_cols():
#     pass