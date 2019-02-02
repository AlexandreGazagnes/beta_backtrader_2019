#!/usr/bin/env python3
# coding: utf-8


# built-in
import os, sys, datetime, time, pickle
from math import pi
from collections import Iterable 
from time import gmtime, strftime 


# data 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc


# visualizitation
import seaborn as sns
from bokeh.sampledata.stocks import MSFT
from bokeh.plotting import figure, show, output_file

# %matplotlib


####################################################################

# check PATH
PATH = os.getcwd()
if PATH[-1] != "/" : 
    PATH += "/"
input(PATH)


# list files
filename = "PX1"
ext = ".csv"
text = str(filename + ext)
input(text)

files = os.listdir(PATH)
files = sorted([i for i in files if ((filename in i) and (ext in i))], reverse=True)
input(files)


# build df 
dfs = [pd.read_csv(PATH + i, sep=";", decimal=",", header=None) for i in files]
df = pd.concat(dfs, axis=0, ignore_index=True)    
del dfs
input(df.head(10))


# manage cols
cols = ["id", "date", "open", "high", "low", "close", "vol"]
df.columns = cols
df.drop(["id", "vol"], axis=1, inplace=True)
input(df.head(10))


# check ohlc integrity
df["_high"] = (df.drop(["date", "high"], axis=1).max(axis=1)) 
df["_low"] =  (df.drop(["date", "low"], axis=1).min(axis=1))
input(df.head(10))

df["_high_integrity"]   = df["high"] >= df["_high"]
df["_low_integrity"]    = df["low"]  <= df["_low"]
_high = (df["_high_integrity"] == True).all()
_low  = (df["_low_integrity"] == True).all()

ohlc = ["open", "high", "low", "close"]
if (not _high) or (not _low) : 
    _df = df.loc[df["_high_integrity"] == False,  ohlc]
    print(_df)
    _df = df.loc[df["_low_integrity"] == False,  ohlc]
    print(_df)
input()

del_cols = [i for i in df.columns if i[0] == "_"]
df.drop(del_cols, axis=1, inplace=True)


# manage date
df["date"] = pd.to_datetime(df.date, dayfirst=True)

assert len(df.date.unique()) == len(df)

# df["_day"] = df.date.apply(lambda i : i.dayofweek)

# days = df.day.unique()
# saturdays = df.loc[df.day == "Saturday" , :].index 
# sundays = df.loc[df.day == "Sunday" , :].index   


# flatten = lambda l: [item for sublist in l for item in sublist]
# df.drop(flatten([saturdays, sundays]), axis=0, inplace=True)
# del saturdays, sundays
# days = df.day.unique()


# sort and index 
df.sort_values("date", axis=0, ascending=True, inplace=True)   
df.index = range(len(df.index))

_df = df.set_index("date", drop=True, inplace=False)
_df.plot()
del _df

# save 
df.to_csv(PATH + filename + ext, sep=",", decimal=".", index=False) 
