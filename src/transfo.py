#!/usr/bin/env python3
# coding: utf-8



# # built-in
# import os, sys, datetime, time, pickle
# from math import pi
# from collections import Iterable 
# from time import gmtime, strftime 


# # data 
# import pandas as pd 
# import numpy as np 
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc


# # visualizitation
# import seaborn as sns
# from bokeh.sampledata.stocks import MSFT
# from bokeh.plotting import figure, show, output_file

# %matplotlib



# dataframe preparation functions
# -----------------------------------------------------------

def random_dataframe(df, random_sel) : 
  
    while True : 
        start = np.random.randint(0, len(df.index)-1)   
        stop  = np.random.randint(start+1, len(df.index))
        if (stop - start) > random_sel.period_min : break
    
    # update randomdf
    df = df.iloc[start : stop, :].copy()
    df.index = list(range(len(df.index))) 

    if random_sel.reverse and np.random.randint(0,2) : 
        raise ValueError("not implemeted")
        code = """
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        """
    df.index = list(range(len(df.index)))

    return df


def week_day_dataframe(df, day) : 
    
    # select day and reindex df
    df = df.loc[df["week_day"] == day, :].copy()
    df.index = list(range(len(df.index)))

    return df


def month_day_dataframe(df, day) : 
    
    # select day and reindex df
    df = df.loc[df["month_day"] == day, :].copy()
    df.index = list(range(len(df.index)))

    return df


def month_dataframe(df, month) : 
    
    # select day and reindex df
    df = df.loc[df["month"] == month, :].copy()
    df.index = list(range(len(df.index)))

    return df


