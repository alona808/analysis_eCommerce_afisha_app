# conda activate tableau_env
# subprocess.run('source activate environment-name && "enter command here" && source deactivate', shell=True)


import os
# os.system("conda run -n tableau_env python helpers.py")

import numpy as np
import pandas as pd
import datetime as dt
import warnings

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
            series = pd.to_datetime(series, format='ISO8601') # format='%Y-%m-%dT%H:%M:%S')
        elif dtype == 'numeric':
            pd.to_numeric(series, errors='ignore')
    except ValueError:
        pass

    return series

def create_calendar_table(start_date, end_date):
    """
    The function creates and returns df calendar table
    """
    df = pd.DataFrame({'date': pd.date_range(start_date, end_date)})
    # week
    df['week_num'] = df['date'].dt.isocalendar().week
    df['week_start_monday'] = df['date'].dt.to_period('W').dt.start_time
    df['week_end'] = df['date'].dt.to_period('W').apply(lambda x: x.end_time).dt.date
    df['year_week'] = df['date'].apply(lambda x: f'{x.isocalendar()[0]}, Week {x.isocalendar()[1]}')
    df['week_range'] = df.apply(lambda x: f"""{x['week_start_monday'].strftime("%b %d, %Y")} to {x['week_end'].strftime("%b %d, %Y")} (Week {x['week_num']})""" , axis=1)
    df['weekday'] = df['date'].dt.strftime("%A")
    df['abbreviated_weekday'] = df['date'].dt.strftime("%a")
    # month
    df['month_start'] = df['date'].to_numpy().astype('datetime64[M]')
    df['month_num'] = df['date'].dt.month
    df['month_year'] = df['date'].dt.strftime("%B %Y")
    # Quater
    df['quarter_number'] = df['date'].dt.quarter
    df['quarter_text'] = df['date'].apply(lambda x: f'Q{x.quarter} {x.strftime("%Y")}')
    # year
    df['year_start'] = df['date'].to_numpy().astype('datetime64[Y]')
    df['year'] = df['date'].dt.isocalendar().year
    
    return df

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
    # return dt.datetime(date.year, date.month, 1)
    return date.to_numpy().astype('datetime64[M]')


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
        year = df[date_column].dt.isocalendar().year
        month = df[date_column].dt.month
        week = df[date_column].dt.isocalendar().week
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
        return ('0 d', 0)
    elif val <= 7:
        return ('7 d', 1)
    elif val <= 14:
        return ('14 d', 2)
    elif val <= 30:
        return ('30 d', 3)
    elif val <= 45:
        return ('45 d', 4)
    elif val <= 60:
        return ('60 d', 5)
    elif val > 60:
        return ('more than 60 d', 6)
    else:
        return ('Never bought', 7)
