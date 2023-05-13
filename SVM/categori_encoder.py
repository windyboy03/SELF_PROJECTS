import pandas as pd
import numpy as np


def category_transform(df, map):
    """
    df(pd.dataFrame) : input dataframe
    map(dict) : category custom map
    """
    for col in df.columns:
        if df[col].dtype == 'object' and col in map:
            df[col] = df[col].map(map[col])
        else:
            df[col] = df[col].map(map[col])
    return df



