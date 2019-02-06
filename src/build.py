#!/usr/bin/env python3
# coding: utf-8



import pandas as pd
import numpy as np
import datetime



# dataFrame init and building functions
# -----------------------------------------------------------

def init_dataframe(filepath, time_sel, delta_max="5 days", enhance_date=True) : 

    # init df
    df = pd.read_csv(filepath)
    df.columns = [i.lower() for i in df.columns]
    if "date" not in df.columns : 
        raise ValueError("please be sure to have a date column")


    # check decimal integrity
    cols = df.columns.drop("date")
    for col in cols : 
        try :       pd.to_numeric(df[col])
        except :    raise TypeError("non numeric columns, convert ',' to '.' ")


    # check ohlc
    if (        (not "open" in df.columns)  or (not "close" in df.columns)
            or  (not "high" in df.columns)  or (not "low" in df.columns)    )  : 

            print("\n\ndataframe columns are : {}".format(df.columns))
            k = input("OHLC format invalid please entre 'f' to force program, other key to stop\n\n")
            if k != "f" : raise KeyboardInterrupt("user choose to quit program")


    # add close_open
    if (("open" and "close") in df.columns) and ("close_open" not in df.columns) : 
        df["close_open"] = (df["open"] + df["close"]) / 2


    # add average
    if (("open" and "high" and "low" and "close") in df.columns) and ("average" not in df.columns) : 
        df["average"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4

   
    # convert date format
    df["date"] = pd.to_datetime(df.date)

    
    # check date integrity
    assert len(df.date.unique()) == len(df)
    df["delta"] = df.date - df.date.shift()
    df = df.loc[df.delta.isna() == False, :]
    
    idxs = df.loc[df.delta > delta_max, :].index
    if len(idxs) : 
        _idxs = np.array([(i-1, i, i+1) for i in idxs]).flatten()
        _idxs = pd.Series(_idxs).sort_values().unique()
        input(df.loc[_idxs, :])
        raise ValueError("ValueError pb missing dates")

    df.drop("delta", axis=1, inplace=True)


    # enhance date
    year_lim=1985

    # handle days of week and month
    if enhance_date and not ("week_day" in df.columns) : 
        df["week_day"] = df.date.apply(lambda i : i.dayofweek)
    if enhance_date and not ("month_day" in df.columns) : 
        df["month_day"] = df.date.apply(lambda i : i.day)
    if enhance_date and not ("month" in df.columns) : 
        df["month"] = df.date.apply(lambda i : i.month) 
    if enhance_date and not ("year" in df.columns) : 
        df["year"] = df.date.apply(lambda i : i.year)

    # check date integrity
    for y in df.year.unique() : 
        if (y < year_lim) or (y >  int(datetime.date.today().year)) :  
            raise ValueError("Date Error : {}".format())
 
 
    # force workdays if needed (crypto vs classic market)
    if not "week_day" in df.columns : 
        raise ValueError("no wek_day in columns")

    if time_sel.force_workdays : 
        idxs = df.loc[df["week_day"] > 4, :].index
        df.drop(idxs, axis=0, inplace=True)
        df.index = list(range(len(df.index)))


    # time selection
    if time_sel.val : 
        
        start = time_sel.start
        stop =  time_sel.stop

        while True : # look random for a good start point
            rand = np.random.choice([-2,-1, 0, 1, 2])
            _start = start[:-1] + str(rand + int(start[-1]))
            _start = pd.to_datetime(_start) 
            _start = df.loc[df.date == _start, :].index
            if len(_start) == 1 :
                break  

        while True : # look random for a good stop point
            rand = np.random.choice([-2,-1, 0, 1, 2])
            _stop = stop[:-1] + str(rand + int(stop[-1]))
            _stop = pd.to_datetime(_stop) 
            _stop = df.loc[df.date == _stop, :].index
            if len(_stop) == 1 :
                break  

        df = df.loc[_start[0] : _stop[0], :].copy()
        df.index = list(range(len(df.index)))   


    # trading_dataframe
    df["long_indicator"]        = 0
    df["short_indicator"]       = 0
    df["long_bank"]             = 0.0
    df["long_quant"]            = 0.0
    df["long_value"]            = 0.0
    df["long_order_quant"]      = 0.0
    df["long_order_value"]      = 0.0
    df["short_bank"]            = 0.0
    df["short_quant"]           = 0.0
    df["short_value"]           = 0.0
    df["short_order_quant"]     = 0.0
    df["short_order_value"]     = 0.0
    df["long_total"]            = 0.0 
    df["short_total"]           = 0.0 
    df["total"]                 = 0.0

    return df


