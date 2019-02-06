#!/usr/bin/env python3
# coding: utf-8



# # built-in
import pickle
# import os, sys, datetime, time, pickle
# from math import pi
from collections import Iterable 
# from time import gmtime, strftime 


# # data 
import pandas as pd 
# import numpy as np 
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc


# # visualizitation
# import seaborn as sns
# from bokeh.sampledata.stocks import MSFT
# from bokeh.plotting import figure, show, output_file

# # %matplotlib



# misc. functions
# -----------------------------------------------------------

def pk_save(data, filename, path) : 

    filename = str(path+filename+".pk")
    with open(filename, 'wb') as f :
        pk = pickle.Pickler(f)
        pk.dump(data)


def pk_load(filename, path) : 

    filename = str(path+filename+".pk")
    with open(filename, 'rb') as f :
        pk = pickle.Unpickler(f)
        return pk .load()


def _clean(path, ext) : 

    files = [f for f in os.listdir(path) if os.path.isfile(path + f)]
    _ = [os.remove(path+i) for i in files if ext in i]


def pk_clean(path) : 
 
    _clean(path, ".pk")


def temp_clean(path) : 
    
    _clean(path, "temp")


def graph_clean(path) : 
    
    _clean(path, ".png")


def master_clean(path) : 

    pk_clean(path)
    temp_clean(path)
    graph_clean(path)


def save_temp_df(df, params, path) : 
    
    assert isinstance(df, pd.DataFrame)
    assert isinstance(params, Iterable)

    d1 = str_timestamp(df.date.iloc[0])
    d2 = str_timestamp(df.date.iloc[-1])
    _day = df.date.iloc[-1].day_name().lower()
    str_list = params
    str_list += [_day, d1, d2]
    filename = ["_" + str(i) for i in str_list] 
    filename = "temp" + "".join(filename) + ".csv"
    df.to_csv(path+filename, index=False)


def str_timestamp(t) : 
    return str(t).replace("-", "").replace(":","").replace(" ", "").replace("000000", "")
