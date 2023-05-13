import numpy as np
import pandas as pd

def train_test_split(data, test_ratio=0.2):
    """
    Args:
        data (DataFrame): The input data to be split.
        test_ratio (float): The ratio of data to be used as test set. Default is 0.2.

    """
    num_samples = len(data)
    test_set_size = int(num_samples * test_ratio)

    test_data = data.iloc[:test_set_size]
    train_data = data.iloc[test_set_size:]

    return train_data, test_data


