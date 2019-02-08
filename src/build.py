#!/usr/bin/env python3
# coding: utf-8



import pandas as pd
import numpy as np
import datetime



# dataFrame init and building functions
# -----------------------------------------------------------

def init_dataframe(filepath, time_sel, enhance_date=True) : 

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
    
    idxs = df.loc[df.delta > time_sel.delta_max, :].index
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
        _start  = pd.to_datetime(time_sel.start)
        _stop   = pd.to_datetime(time_sel.stop)

        if _start < df.date.iloc[0]  : _start = df.date.iloc[0]
        if _stop  > df.date.iloc[-1] : _stop  = df.date.iloc[-1]

        while True:
            if len(df.loc[df.date == _start, : ].index) == 1 : 
                _start_idx = df.loc[df.date == _start].index[0]
                break
            _start += pd.Timedelta(1, unit="D")

        while True:
            if len(df.loc[df.date == _stop, : ].index) == 1: 
                _stop_idx  = df.loc[df.date == _stop ].index[0] 
                break
            _stop -= pd.Timedelta(1, unit="D")


        df = df.iloc[_start_idx : _stop_idx, :]
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


