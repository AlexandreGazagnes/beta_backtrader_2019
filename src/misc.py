#!/usr/bin/env python3
# coding: utf-8



# # built-in
import pickle
import os # sys, datetime, time, pickle
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


def time_to_str_timestamp(t) : 
    return str(t).replace("-", "").replace(":","").replace(" ", "").replace("000000", "")

def time_to_int_timestamp(t) : 
    return int(str(t).replace("-", "").replace(":","").replace(" ", "").replace("000000", ""))

def time_to_float_period(t) : 
    t0 = str(t[0]).replace("-", "").replace(":","").replace(" ", "").replace("000000", "")
    t1 = str(t[1]).replace("-", "").replace(":","").replace(" ", "").replace("000000", "")
    return float(t0+"."+t1)

def float_to_time_period(t) : 
    
    assert isinstance(t, float)
    t0, t1 = str(t).split(".")
    t0, t1 = t0[:4]+"-"+t0[4:6]+"-"+t0[6:], t0[:4]+"-"+t1[4:6]+"-"+t1[6:]

    return (pd.Timestamp(t0), pd.Timestamp(t1))


# def chunks(l, n):

#     from math import ceil

#     n = len(l)/n
#     n = ceil(n)
    
#     """Yield successive n-sized chunks from l."""
#     for i in range(0, len(l), n):
#         yield l[i:i + n]



def chunks(l, n) : 
    from math import ceil
    numbs =  [ceil(i) for i in np.linspace(0,len(l)+1, n+1)]    
    pairs = list()
    for i, val in enumerate(numbs) : 
        try : 
            pairs.append((numbs[i], numbs[i+1]))
        except : 
            return pairs


