#!/usr/bin/env python3
# coding: utf-8



# # built-in
# import os, sys, datetime, time, pickle
# from math import pi
# from collections import Iterable 
# from time import gmtime, strftime 


# # data 
import pandas as pd 
# import numpy as np 
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc



# trading functions
# -----------------------------------------------------------

def do_nothing(df, i, _type, mkt_price) : 

    assert isinstance(_type, str)
    assert _type in ["long", "short"]
    assert isinstance(mkt_price, str)
    assert mkt_price in ["open", "close", "average", "clos_op"]

    try :     
        df.loc[i, _type + "_bank"]          = df.loc[i-1, _type + "_bank"]
        df.loc[i, _type + "_quant"]         = df.loc[i-1, _type + "_quant"]
        df.loc[i, _type + "_order_quant"]   = 0.0
        df.loc[i, _type + "_value"]          = df.loc[i, _type + "_quant"] * df.loc[i, mkt_price]
        df.loc[i, _type + "_order_value"]    = 0.0
    except : 
        raise ValueError("do nothing error", str(i), _type, mkt_price)

    return df 
    

def long_buy(df, i, trd_pm, broker) : 

    if (not trd_pm.long.open_trade) or (trd_pm.multi_trade.enable): 

        if trd_pm.long.size_type == "val" : 
            position_size = trd_pm.long.size_val
        elif trd_pm.long.size_type == "%" : 
            position_size = trd_pm.long.size_val * df.loc[i, "long_bank"]
        else : 
            raise ValueError("trd_pm.long.size type or val error")

        df.loc[i, "long_bank"] -= position_size
        price = df.loc[i, trd_pm.price.mkt]
        quant = position_size * (1 - broker.spread) * (1 - broker.fees) / price

        df.loc[i, "long_quant"]         += quant
        df.loc[i, "long_order_quant"]   = quant
        df.loc[i, "long_value"]         = df.loc[i, "long_quant"] * price
        df.loc[i, "long_order_value"]   = quant * price

        trd_pm.long.last_buy            = price
        trd_pm.long.open_trade          = True
 
    return df, trd_pm


def long_stop_profit(df, i, trd_pm, broker) : 

    if (trd_pm.long.open_trade) or (trd_pm.multi_trade.enable): 
        
        quant                           = df.loc[i, "long_quant"]
        price                           = df.loc[i, trd_pm.price.mkt]
        bank                            =   quant * price * (1 - broker.spread) \
                                          * (1 - broker.fees)
        
        df.loc[i, "long_quant"]         = 0.0
        df.loc[i, "long_order_quant"]   =  - quant
        df.loc[i, "long_value"]         = 0.0
        df.loc[i, "long_order_value"]   =  - bank
        df.loc[i, "long_bank"]          = bank 
        
        trd_pm.long.last_buy            = -1
        trd_pm.long.open_trade          = False
    
    return df, trd_pm


def long_stop_loss(df, i, trd_pm, broker) : 

    if trd_pm.long.open_trade and (trd_pm.long.last_buy > df.loc[i, trd_pm.price.mkt]): 

        quant                           = df.loc[i, "long_quant"]
        price                           = df.loc[i, trd_pm.price.mkt]
        bank                            =   quant * price * (1 - broker.spread) \
                                          * (1 - broker.fees)
        
        df.loc[i, "long_quant"]         = 0.0
        df.loc[i, "long_order_quant"]   =  - quant
        df.loc[i, "long_value"]         = 0.0
        df.loc[i, "long_order_value"]   =  - bank
        df.loc[i, "long_bank"]          = bank 
        
        trd_pm.long.last_buy            = -1
        trd_pm.long.open_trade          = False
    
    return df, trd_pm


def short_buy(df, i, trd_pm, broker) :

    if (not trd_pm.short.open_trade) or (trd_pm.multi_trade.enable): 

        if trd_pm.short.size_type == "val" : 
            position_size = trd_pm.short.size_val
        elif trd_pm.short.size_type == "%" : 
            position_size = trd_pm.short.size_val * df.loc[i, "short_bank"]
        else : 
            raise ValueError("trd_pm.short.size type or val error")


        price = df.loc[i, trd_pm.price.mkt]
        quant = position_size * (1 - broker.spread) * (1 - broker.fees) / price
        df.loc[i, "short_bank"] += quant * price

        df.loc[i, "short_quant"]         -= quant
        df.loc[i, "short_order_quant"]   = -quant
        df.loc[i, "short_value"]         = df.loc[i, "short_quant"] * price
        df.loc[i, "short_order_value"]   = - quant * price

        trd_pm.short.last_buy            = price
        trd_pm.short.open_trade          = True

    return df, trd_pm


def short_stop_profit(df, i, trd_pm, broker): 

    if (trd_pm.short.open_trade) or (trd_pm.multi_trade.enable): 

        quant                           = df.loc[i, "short_quant"]
        price                           = df.loc[i, trd_pm.price.mkt]
        bank                            =   quant * price * (1 + broker.spread) \
                                          * (1 + broker.fees)
        
        df.loc[i, "short_quant"]         -= quant
        df.loc[i, "short_order_quant"]   =  -quant
        df.loc[i, "short_value"]         = df.loc[i, "short_quant"] * price
        df.loc[i, "short_order_value"]   =  df.loc[i, "short_quant"] * price
        df.loc[i, "short_bank"]          += bank
        
        trd_pm.short.last_buy            = -1
        trd_pm.short.open_trade          = False

    return df, trd_pm


def short_stop_loss(df, i, trd_pm, broker) : 

    if (trd_pm.short.open_trade) and (trd_pm.short.last_buy < df.loc[i, trd_pm.price.mkt]) : 
        
        quant                           = df.loc[i, "short_quant"]
        price                           = df.loc[i, trd_pm.price.mkt]
        bank                            =   quant * price * (1 + broker.spread) \
                                          * (1 + broker.fees)
            
        df.loc[i, "short_quant"]         -= quant
        df.loc[i, "short_order_quant"]   =  -quant
        df.loc[i, "short_value"]         = df.loc[i, "short_quant"] * price
        df.loc[i, "short_order_value"]   = -quant * price
        df.loc[i, "short_bank"]          += bank
        
        trd_pm.short.last_buy            = -1
        trd_pm.short.open_trade          = False

    return df, trd_pm


def trading_room(df, trading_params, broker) : 

    assert isinstance(df, pd.DataFrame)

    for _, i in enumerate(df.index) : # trading loop

        if trading_params.first:  # first
            df.loc[i, "long_bank"]  = trading_params.long.bank_init
            df.loc[i, "short_bank"] = trading_params.short.bank_init
            trading_params.first = False
            continue

        # do nothing
        df = do_nothing(df, i, "long", trading_params.price.mkt)
        df = do_nothing(df, i, "short", trading_params.price.mkt)


        # long
        if trading_params.long.enable : 
            if df.loc[i, "long_indicator"] == 2 : # buy
                df, trading_params = long_buy(df, i, trading_params, broker) 
            elif df.loc[i, "long_indicator"] == -2 : # stop profit
                df, trading_params = long_stop_profit(df, i, trading_params, broker)
            elif df.loc[i, "long_indicator"] == -1 :  # stop loss
                df, trading_params = long_stop_loss(df, i, trading_params, broker) 


        # short
        if trading_params.short.enable : 
            if df.loc[i, "short_indicator"] == 2 : # buy
                df, trading_params = short_buy(df, i, trading_params, broker) 
            elif df.loc[i, "short_indicator"] == -2 : # stop profit
                df, trading_params = short_stop_profit(df, i, trading_params, broker)
            elif df.loc[i, "short_indicator"] == -1 :  # stop loss
                df, trading_params = short_stop_loss(df, i, trading_params, broker) 


    # last round force to sell ! 
    i = df.index[-1]
    df, trading_params = long_stop_profit(df, i, trading_params, broker)
    df, trading_params = short_stop_profit(df, i, trading_params, broker)

    df["long_total"] = df.long_bank + df.long_value
    df["short_total"] = df.short_bank + df.short_value
    df["total"] = df.long_total + df.short_total
    
    return df, trading_params


def compute_trading_results(df, ref_price) : 

    market_start = df[ref_price].iloc[0]
    market_stop  = df[ref_price].iloc[-1]
    market_results = round((market_stop - market_start) / market_start, 2)

    trade_start = df["total"].iloc[0]
    trade_stop  = df["total"].iloc[-1]
    trade_results = round((trade_stop - trade_start) / trade_start, 2)

    return (trade_results, market_results)


def compare_trading_vs_market_results(df) : 
    pass