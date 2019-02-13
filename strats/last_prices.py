#!/usr/bin/env python3
# coding: utf-8



import pandas as pd



# Last prices Strategy
# -----------------------------------------------------------

def strategy(df, trd_params, last_prices, max_last_prices=10) :

    # args check
    if not isinstance(df, pd.DataFrame) : 
        raise TypeError("'df' must be a pd.DataFrame object")
    assert isinstance(last_prices, int)
    assert ((last_prices >=1) and (last_prices <=max_last_prices))

    # build last prices
    ref_p = trd_params.price.ref
    for i in range(1, 1+last_prices) : 
        df["last_"+str(i)+"_week"]  = round(100 *  (df[ref_p] - df[ref_p].shift(i)) / df[ref_p].shift(i),2)

    # build primary indicators
    cols                            = [ i for i in df.columns if "last" in i]
    df["all_green"]                 = (df.loc[:, cols] > 0).all(axis = 1)
    df["all_red"]                   = (df.loc[:, cols] < 0).all(axis = 1)

    # def long_buy, long_stop_loss, long_stop_profit
    if trd_params.long.enable : 
        df.loc[df["all_green"]      == True , "long_indicator"]   =  2
        df.loc[df["last_1_week"]    <  0, "long_indicator"]       = -1
        df.loc[df["all_red"]        == True, "long_indicator"]    = -2

    # def short_buy, short_stop_loss, short_stop_profit
    if trd_params.short.enable : 
        df.loc[df["all_red"]        == True, "short_indicator"]   =  2
        df.loc[df["last_1_week"]    >  0, "short_indicator"]      = -1
        df.loc[df["all_green"]      == True , "short_indicator"]  = -2

    # drop ligns without indicators
    df = df.iloc[last_prices:, :].copy()
    df.index = list(range(len(df.index)))

    return df
