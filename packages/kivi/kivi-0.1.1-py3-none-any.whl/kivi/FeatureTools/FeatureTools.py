# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 08:58
# @Author  : Chensy Cao
# @Email   : chensy.cao@zjtlcb.com
# @FileName: FeatureTools.py
# @Software: PyCharm

import numpy as np
import pandas as pd


def ratio(df: pd.DataFrame, dividend: str, divisor: str, new_col: str):
    df[new_col] = df[dividend] / df[divisor]


def cross_nan(item):
    if np.isnan(item[cols[0]]) and np.isnan(item[cols[1]]):
        return "A"
    elif np.isnan(item[cols[0]]) and (not np.isnan(item[cols[1]])):
        return "B"
    elif (not np.isnan(item[cols[0]])) and np.isnan(item[cols[1]]):
        return "C"
    else:
        return "D"


def cross_median(item, ):
    """
    median_a 月份数
    median_b 融资次数
    :param item:
    :return:
    """
    if (item[cols[0]] <= median_a) and (item[cols[1]] <= median_b):
        return 2
    elif (item[cols[0]] <= median_a) and (item[cols[1]] > median_b):
        return 3
    elif (item[cols[0]] > median_a) and (item[cols[1]] <= median_b):
        return 5
    elif (item[cols[0]] > median_a) and (item[cols[1]] > median_b):
        return 4
    else:
        return 1


def joint_feature(df, corss_type, med_a=None, med_b=None, dropna=False):
    global cols, median_a, median_b

    if dropna == True:
        df.dropna(axis=0, inplace=True)

    cols = df.columns.tolist()
    target_name = cols.pop(-1)
    if med_a is not None:
        median_a = med_a
        median_b = med_b
    else:
        median_a = df[cols[0]].median()
        median_b = df[cols[1]].median()
    if corss_type == 'nan':
        df['corr'] = df.apply(cross_nan, axis=1)
    elif corss_type == 'median':
        df['corr'] = df.apply(cross_median, axis=1)
    return df
