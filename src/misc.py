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



