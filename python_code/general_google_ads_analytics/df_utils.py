from typing import List
import numpy as np
import pandas as pd
from typing import TypedDict


class CalculatedColumn(TypedDict):
    divide_left: str
    divide_right: str
    new_name: str


def add_divided_column(df: pd.DataFrame, cols: List[CalculatedColumn]) -> pd.DataFrame:
    """
    :param df: source dataframe
    :param cols: args for the new fields
    :return:
    """
    for item in cols:
        df[item['new_name']] = df[item['divide_left']] / df[item['divide_right']]
    df = df.replace([np.inf, -np.inf], 0)
    df.fillna(value=0, inplace=True)
    return df


def normalize_cost_micros(df: pd.DataFrame) -> pd.DataFrame:
    df['cost'] = df['metrics.cost_micros'] * .000001
    return df


def convert_impression_data(df: pd.DataFrame) -> pd.DataFrame:
    df['impression_volume'] = df['metrics.impressions'] / df['metrics.search_impression_share']
    df['top_impressions'] = df['metrics.impressions'] * df['metrics.search_top_impression_share']
    df['abs_top_impressions'] = df['metrics.impressions'] * df['metrics.search_absolute_top_impression_share']

    del df['metrics.search_impression_share']
    del df['metrics.search_top_impression_share']
    del df['metrics.search_absolute_top_impression_share']

    return df
