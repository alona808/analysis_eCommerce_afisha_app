import os

import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import warnings
import pandas as pd
import numpy as np
import logging as log
import datetime as dt

# from scipy import stats
# from scipy.stats import mode

# import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='white')


# to show warnings only once:
warnings.filterwarnings(action='once')


def summary_stats(df):
    """
    The function takes a data frame as input and calculates
    summary statistics to reveal the understanding of the data
    in each column.
    The function returns a data frame where each feature
    in the data set is a row and the summary statistics are columns.
    """
    eda = {}
    eda['dtype'] = df.dtypes
#     eda['mamory_usage'] = df.memory_usage('deep')
    eda['count'] = df.count()
    eda['min'] = df.min()
    eda['mean'] = df.mean()
    eda['median'] = df.median()
    eda['std'] = df.std()
    eda['max'] = df.max()
    eda['skew'] = df.skew(skipna=True)
    eda['null_sum'] = df.isnull().sum()
    eda['null_%'] = round((df.isnull().mean() * 100), 2)
    return pd.DataFrame(eda)


def dtype_converter(series, dtype):
    """
    The function converts data type of series to another.
    And returns series.
    """
    types_data = ['int', 'float', 'float64', 'bool', 'str', 'category']
    try:
        if any(elem in dtype for elem in types_data):
            series = series.astype(dtype)
        elif dtype == 'date':
            series = pd.to_datetime(series, format='%Y-%m-%dT%H:%M:%S')
        elif dtype == 'numeric':
            pd.to_numeric(series, errors='ignore')
    except ValueError:
        pass

    return series


def time_diff(end_ts, start_ts, time_val):
    """
    The function returns a difference between two timestamp in time_val
    """
    try:
        if time_val == 'seconds':
            return (end_ts - start_ts).dt.seconds
        elif time_val == 'days':
            return (end_ts - start_ts).dt.days
        elif time_val == 'week':
            return (end_ts - start_ts).dt.week
        elif time_val == 'month':
            return (end_ts - start_ts).dt.month
        elif time_val == 'year':
            return (end_ts - start_ts).dt.year

    except ValueError:
        'Data type is not datetime64[ns]'


def get_month(date):
    """
    The function truncates the given date in the column
    to the year and the first day of the month
    """
    return dt.datetime(date.year, date.month, 1)


def get_day(df, date_column):
    """
    The function retrives day from the `date_column` and
    returns it in datetime64[ns] format.
    """
    return pd.to_datetime(df[date_column].dt.date)


def get_date_int(df, date_column):
    """
    The function retrives year, month, week, day from the `date_column`
    and returns int num of them
    """
    try:
        year = df[date_column].dt.year
        month = df[date_column].dt.month
        week = df[date_column].dt.strftime('%V')
        day = df[date_column].dt.date
        dayofweek = df[date_column].dt.dayofweek
    except ValueError:
        'Data column is not datetime64[ns]'

    return year, month, week, day, dayofweek

def round_seconds(obj: dt.datetime) -> dt.datetime:
    """
    """
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)



def conversion_group(val):
    """
    The function categorizes the series
    """
    if val == 0:
        return 0
    elif val <= 7:
        return '7 d'
    elif val <= 14:
        return '14 d'
    elif val <= 30:
        return '30 d'
    elif val > 30:
        return 'more than 30 d'
    else:
        return 'Never bought'

    
def write_df_to_csv(df, file_path_local):
    """
    Function writes DataFrame to csv file
    """
    df.to_csv(file_path_local, header='column_names', index=False, sep=',',  encoding='utf-8')
    log.info(f'DataFrame is written to {file_path_local}')

    