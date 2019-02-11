#!/usr/bin/env python3
# coding: utf-8



# # built-in
# import os, sys, datetime, time, pickle
# from math import pi
from collections import Iterable 
# from time import gmtime, strftime 


# # data 
import pandas as pd 
import numpy as np 
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc


# # visualizitation
# import seaborn as sns
# from bokeh.sampledata.stocks import MSFT
# from bokeh.plotting import figure, show, output_file

# %matplotlib



# dataframe preparation functions
# -----------------------------------------------------------

def set_ref_prices(df) : 

    auth = ["open", "close", "average", "clos_op"]
    return [i for i in df.columns if i in auth]


def set_ref_days(df) : 
    
    if not "week_day" in df.columns : 
        raise ValueError("no wek_day in columns")

    return sorted(df.week_day.unique()) 


def set_rand_periods(df, random_sel) : 

    rand_periods = list()

    if not random_sel.val : 
        return [(df.iloc[0].loc["date"], df.iloc[-1].loc["date"]),]

    for _ in range(random_sel.nb) : 
        while True : 
            start = np.random.randint(0, len(df.index)-1)   
            stop  = np.random.randint(start+1, len(df.index))
            stop_start = (stop - start) 
            if ((stop_start >= random_sel.period_min) and (stop_start <= random_sel.period_max) ) : 
                break

        start = df.iloc[start].loc["date"]
        stop  = df.iloc[stop].loc["date"]

        rand_periods.append((start, stop))

    return rand_periods


def random_dataframe(df, start_stop) : 

    assert isinstance(start_stop, Iterable)
    assert len(start_stop) == 2
    for i in start_stop : 
        assert isinstance(i, pd.Timestamp) 

    # update randomdf
    start, stop = start_stop[0], start_stop[1]
    idx_start   = df.loc[df.date == start, :].index[0]
    idx_stop    = df.loc[df.date == stop, :].index[0]

    df = df.iloc[idx_start : idx_stop, :]
    df.index = list(range(len(df.index)))

    return df


def week_day_dataframe(df, day) : 
    
    # select day and reindex df
    df = df.loc[df["week_day"] == day, :]
    df.index = list(range(len(df.index)))

    return df


def month_day_dataframe(df, day) : 
    
    # select day and reindex df
    df = df.loc[df["month_day"] == day, :]
    df.index = list(range(len(df.index)))

    return df


def month_dataframe(df, month) : 
    
    # select day and reindex df
    df = df.loc[df["month"] == month, :]
    df.index = list(range(len(df.index)))

    return df


