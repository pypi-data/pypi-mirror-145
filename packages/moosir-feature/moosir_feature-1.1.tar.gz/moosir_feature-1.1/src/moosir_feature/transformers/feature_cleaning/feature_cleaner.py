"""
todo:
    - there is way more ways of removing outliers:  Peirce criterion, Grubb's test or Dixon's Q-test, clusters, zscore, ...


"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def clip_quantile(features: pd.DataFrame, lower_quantile=0.01, upper_quantile=0.99):
    return features.clip(features.quantile(lower_quantile), features.quantile(upper_quantile), axis=1)


def timestamp_resample(data: pd.DataFrame, resample_freq: str) -> pd.DataFrame:
    # never use last() cos it hints the model for future
    data.index = pd.to_datetime(data.index)

    resampled = (data
                 .groupby(pd.Grouper(freq=resample_freq))
                 .first()
                 .dropna(how="all")
                 )
    return resampled


def convert_to_pips(data: pd.DataFrame):
    return data.round(4).sub(1).mul(10000)


def apply_basic_cleaning(instances: pd.DataFrame, resample_freq: str):
    # basic transforms
    result = instances.copy()
    result = timestamp_resample(data=result, resample_freq=resample_freq)
    result = convert_to_pips(data=result)

    return result


def standardize(data: pd.DataFrame):
    """
    rescale all values to be have mean = 0 and std = 1
    z = (x- mean) / std
    Note:
        - Better not to use it cuz of any normalize assumption to financial data is dangerous (todo: to be confirmed)!!!
        - THE RESULT WILL BE NORMAL DISTRIBUTION
        - standard deviation and mean changed (unlike normalization)
        - z-score standardization
        - good for comparing data with different UoM
        - must for gradient descent based

    """
    raise Exception("Not implemented!!")


def normalize(data: pd.DataFrame):
    """
      rescale all values to be [0,1]
      z = (X - Xmin) / Xmax - Xmin
      Note:
          - DOES NOT change the distribution of the result
          - standard deviation and mean is not changed (unlike standardize)
          - MinMaxScaling is normalization
          - can suppress the effect of outliers (not sure)??
          - must for gradient descent based
          - not required for decision trees
          - you should scale target variable too!!!
      :param target_col: just to make sure that target col is not in this process
      """

    scaler = MinMaxScaler()
    scaler.fit(data)
    transformed = scaler.transform(data)

    transformed_df = pd.DataFrame(data=transformed, index=data.index, columns=data.columns)
    return transformed_df, scaler

