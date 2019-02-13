#!/usr/bin/env python3
# coding: utf-8



# # built-in
# import os, sys, datetime, time, pickle
# from math import pi
# from collections import Iterable 
# from time import gmtime, strftime
from logging import warning

# # data 
import pandas as pd 
# import numpy as np 
# import matplotlib.pyplot as plt
# from mpl_finance import candlestick_ohlc



# trading functions
# -----------------------------------------------------------

def do_nothing(df, i, _type, trd_params) : 

    # args check
    mkt_price = trd_params.price.mkt
    assert isinstance(_type, str)
    assert _type in ["long", "short"]
    assert isinstance(mkt_price, str)
    assert mkt_price in ["open", "close", "average", "clos_op"]

    # bank
    if trd_params.bank.dual : 
        df.loc[i, _type + "_bank"]              = df.loc[i-1, _type + "_bank"]
    else : 
        df.loc[i, "bank"]                       = df.loc[i-1, "bank"]

    # order
    try :     
        df.loc[i, _type + "_quant"]             = df.loc[i-1, _type + "_quant"]
        df.loc[i, _type + "_order_quant"]       = 0.0
        df.loc[i, _type + "_value"]             = df.loc[i, _type + "_quant"] * df.loc[i, mkt_price]
        df.loc[i, _type + "_order_value"]       = 0.0
    except : 
        raise ValueError("do nothing error", str(i), _type, mkt_price)

    return df 
    

def long_buy(df, i, trd_pm, broker) : 

    # args check
    if trd_pm.bank.dual :   _bank               = "long_bank"
    else :                  _bank               = "bank"
    
    # position size
    if (not trd_pm.long.open_trade) or (trd_pm.multi_trade.enable): 

        if trd_pm.long.size_type == "val" : position_size = trd_pm.long.size_val
        elif trd_pm.long.size_type == "%" : position_size = trd_pm.long.size_val * df.loc[i, _bank]
        else :                              raise ValueError("trd_pm.long.size type or val error")

        df.loc[i, _bank]                       -= position_size
        price                                   = df.loc[i, trd_pm.price.mkt]
        quant                                   = position_size * (1 - broker.spread) * (1 - broker.fees) / price

        df.loc[i, "long_quant"]                += quant
        df.loc[i, "long_order_quant"]           = quant
        df.loc[i, "long_value"]                 = df.loc[i, "long_quant"] * price
        df.loc[i, "long_order_value"]           = quant * price

        #        warning(str(price))
        #        warning(str(type(price)))

        # assert (isinstance(price, float) or isinstance(price, int))
        trd_pm.long.last_buy                    = price
        trd_pm.long.open_trade                  = True
 
    return df, trd_pm


def long_stop_profit(df, i, trd_pm, broker) : 

    # args check
    if trd_pm.bank.dual :   _bank = "long_bank"
    else :                  _bank = "bank"

    # position size 
    if (trd_pm.long.open_trade) or (trd_pm.multi_trade.enable): 
        
        quant                                   = df.loc[i, "long_quant"]
        price                                   = df.loc[i, trd_pm.price.mkt]
        bank                                    = quant * price * (1 - broker.spread) \
                                                  * (1 - broker.fees)
        
        df.loc[i, "long_quant"]                 = 0.0
        df.loc[i, "long_order_quant"]           = -quant
        df.loc[i, "long_value"]                 = 0.0
        df.loc[i, "long_order_value"]           = -bank
        df.loc[i, _bank]                        = bank 
        
        trd_pm.long.last_buy                    = 0.0
        trd_pm.long.open_trade                  = False
    
    return df, trd_pm


def long_stop_loss(df, i, trd_pm, broker) : 

    if trd_pm.bank.dual :   _bank = "long_bank"
    else :                  _bank = "bank"

    if trd_pm.long.open_trade and (trd_pm.long.last_buy > df.loc[i, trd_pm.price.mkt]): 

        quant                                   = df.loc[i, "long_quant"]
        price                                   = df.loc[i, trd_pm.price.mkt]
        bank                                    = quant * price * (1 - broker.spread) \
                                                  * (1 - broker.fees)
        
        df.loc[i, "long_quant"]                 = 0.0
        df.loc[i, "long_order_quant"]           = -quant
        df.loc[i, "long_value"]                 = 0.0
        df.loc[i, "long_order_value"]           = -bank
        df.loc[i, _bank]                        = bank 
        
        trd_pm.long.last_buy                    = 0.0
        trd_pm.long.open_trade                  = False
    
    return df, trd_pm


def short_buy(df, i, trd_pm, broker) :

    if trd_pm.bank.dual :   _bank = "short_bank"
    else :                  _bank = "bank"

    if (not trd_pm.short.open_trade) or (trd_pm.multi_trade.enable): 

        if trd_pm.short.size_type == "val" : 
            position_size                       = trd_pm.short.size_val
        elif trd_pm.short.size_type == "%" : 
            position_size                       = trd_pm.short.size_val * df.loc[i, _bank]
        else : 
            raise ValueError("trd_pm.short.size type or val error")

        price                                   = df.loc[i, trd_pm.price.mkt]
        quant                                   = position_size * (1 - broker.spread) * (1 - broker.fees) / price
        df.loc[i, _bank]                       += quant * price

        df.loc[i, "short_quant"]               -= quant
        df.loc[i, "short_order_quant"]          = -quant
        df.loc[i, "short_value"]                = df.loc[i, "short_quant"] * price
        df.loc[i, "short_order_value"]          = -quant * price

        #        warning(str(price))
        #        warning(str(type(price)))

        # assert (isinstance(price, float) or isinstance(price, int))
        trd_pm.short.last_buy                   = price
        trd_pm.short.open_trade                 = True

    return df, trd_pm


def short_stop_profit(df, i, trd_pm, broker): 

    if trd_pm.bank.dual :   _bank = "short_bank"
    else :                  _bank = "bank"

    if (trd_pm.short.open_trade) or (trd_pm.multi_trade.enable): 

        quant                                   = df.loc[i, "short_quant"]
        price                                   = df.loc[i, trd_pm.price.mkt]
        bank                                    = quant * price * (1 + broker.spread) \
                                                    * (1 + broker.fees)
        
        df.loc[i, "short_quant"]               -= quant
        df.loc[i, "short_order_quant"]          = -quant
        df.loc[i, "short_value"]                = df.loc[i, "short_quant"] * price
        df.loc[i, "short_order_value"]          = df.loc[i, "short_quant"] * price
        df.loc[i, _bank]                       += bank
        
        trd_pm.short.last_buy                   = 0.0
        trd_pm.short.open_trade                 = False

    return df, trd_pm


def short_stop_loss(df, i, trd_pm, broker) : 

    if trd_pm.bank.dual :   _bank = "short_bank"
    else :                  _bank = "bank"

    if (trd_pm.short.open_trade) and (trd_pm.short.last_buy < df.loc[i, trd_pm.price.mkt]) : 
        
        quant                                   = df.loc[i, "short_quant"]
        price                                   = df.loc[i, trd_pm.price.mkt]
        bank                                    = quant * price * (1 + broker.spread) \
                                                    * (1 + broker.fees)
            
        df.loc[i, "short_quant"]               -= quant
        df.loc[i, "short_order_quant"]          = -quant
        df.loc[i, "short_value"]                = df.loc[i, "short_quant"] * price
        df.loc[i, "short_order_value"]          = -quant * price
        df.loc[i, _bank]                       += bank
        
        trd_pm.short.last_buy                   = 0.0
        trd_pm.short.open_trade                 = False

    return df, trd_pm


def long_block(df, i, trd_params, broker) :

    if df.loc[i, "long_indicator"] == 2 : # buy
        df, trd_params = long_buy(df, i, trd_params, broker) 
    elif df.loc[i, "long_indicator"] == -2 : # stop profit
        df, trd_params = long_stop_profit(df, i, trd_params, broker)
    elif df.loc[i, "long_indicator"] == -1 :  # stop loss
        df, trd_params = long_stop_loss(df, i, trd_params, broker)

    return df, trd_params


def short_block(df, i, trd_params, broker) :

    if df.loc[i, "short_indicator"] == 2 : # buy
        df, trd_params = short_buy(df, i, trd_params, broker) 
    elif df.loc[i, "short_indicator"] == -2 : # stop profit
        df, trd_params = short_stop_profit(df, i, trd_params, broker)
    elif df.loc[i, "short_indicator"] == -1 :  # stop loss
        df, trd_params = short_stop_loss(df, i, trd_params, broker) 

    return df, trd_params


def trading_room(df, trd_params, broker) : 

    assert isinstance(df, pd.DataFrame)

    for _, i in enumerate(df.index) : # trading loop

        # first
        if trd_params.first:  # first
            if trd_params.bank.dual : 
                if trd_params.long.enable : df.loc[i, "long_bank"]  = trd_params.bank.long_init
                if trd_params.long.enable : df.loc[i, "short_bank"] = trd_params.bank.short_init
            else : 
                df.loc[i, "bank"]  = trd_params.bank.init

            trd_params.first = False
            continue

        # do nothing
        if trd_params.long.enable  :        df = do_nothing(df, i, "long", trd_params)   
        if trd_params.short.enable :        df = do_nothing(df, i, "short", trd_params)

        # orders
        if trd_params.bank.dual : # orders order do nout count, long then short == short then long
            
            # long and short 
            if trd_params.long.enable :     df, trd_params = long_block(df, i, trd_params, broker) 
            if trd_params.short.enable :    df, trd_params = short_block(df, i, trd_params, broker)

        else : # orders order do count, long then short != short then long
            
            if ( (not trd_params.long.open_trade) and (not trd_params.short.open_trade ) ) : 
                if trd_params.long.enable : df, trd_params = long_block(df, i, trd_params, broker) 
                if trd_params.short.enable: df, trd_params = short_block(df, i, trd_params, broker)
            
            elif  ( (trd_params.long.open_trade) and (trd_params.short.open_trade ) ) : 
                raise ValueError("Long and Short pos. opened in the same time")
            
            elif  ( (trd_params.long.open_trade) and (not trd_params.short.open_trade ) ) : 
                if trd_params.long.enable : df, trd_params = long_block(df, i, trd_params, broker) 
                if trd_params.short.enable: df, trd_params = short_block(df, i, trd_params, broker)
            
            elif  ( (not trd_params.long.open_trade) and (trd_params.short.open_trade ) ) : 
                if trd_params.short.enable: df, trd_params = short_block(df, i, trd_params, broker)
                if trd_params.long.enable : df, trd_params = long_block(df, i, trd_params, broker) 
            
            else : 
                raise ValueError("Something went wrong")


    # last round force to sell ! 
    i = df.index[-1]
    if trd_params.long.enable :
        df, trd_params                  = long_stop_profit(df, i, trd_params, broker)
    if trd_params.short.enable :
        df, trd_params                  = short_stop_profit(df, i, trd_params, broker)

    # handle long/short total 
    if trd_params.bank.dual : 
        if trd_params.long.enable : 
            df["long_total"]            = df.long_bank + df.long_value
            df["total"]                 = df.long_total
        if  trd_params.short.enable : 
            df["short_total"]           = df.short_bank + df.short_value
            df["total"]                 = df.short_total
        if trd_params.long.enable and trd_params.short.enable : 
            df["total"]                 = df.long_total + df.short_total
    else : 
        if trd_params.long.enable : 
            df["total"]                 = df.bank + df.long_value
        if trd_params.short.enable : 
            df["total"]                 = df.bank + df.short_value
        if trd_params.long.enable and trd_params.short.enable : 
            df["total"]                 = df.bank + df.long_value + df.short_value
    
    return df, trd_params


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