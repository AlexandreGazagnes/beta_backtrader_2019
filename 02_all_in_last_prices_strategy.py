#!/usr/bin/env python3
# coding: utf-8



####################################################################
####################################################################

#    BBBB : Baby Boring Backtrader is Back

####################################################################
####################################################################




####################################################################
#       IMPORT
####################################################################


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

%matplotlib
sns.set()


# src
from src.misc import *
from src.build import * 
from src.transfo import *
#from src.consts import *
from src.params import * 
from src.trading import *
from strats import * 


####################################################################
#       CONSTANTS
####################################################################


# paths
paths = Path(C.PATH, C.FILE)
# paths.data_file = '/home/alex/Downloads/ABC_bourse/data/eth_usd_ethermine_ok.csv'

# broker params
broker = Broker(C.FEES, C.SPREAD, C.ROLL_OVER)

# time selection
# time_sel = TimeSel(C.TIME_SELECT, C.TIME_START, C.TIME_STOP)
time_sel = TimeSel(False, "2012-01-13", "2019-01-04")

# random selection
# random_sel = RandomSel(C.RANDOMIZE, C.RANDOM_NB, C.RANDOM_PERIOD_MIN, C.ENABLE_REVERSE)
random_sel = RandomSel(False, 1, 400, False)

# Output
output = Output(C.GRAPHS, C.TEMP_FILES, C.PRINT_RESULTS, paths.temp_path)

# tradings params
# trading_params = TradingParams( C.VERSION, C.ENABLE_MULTI_TRADE, C.ENABLE_LONG, C.ENABLE_SHORT, 
#                                 C.MULTI_TRADE_MAX, 
#                                 C.LONG_BANK_INIT, C.LONG_SIZE_VAL, C.LONG_SIZE_TYPE,
#                                 C.SHORT_BANK_INIT, C.SHORT_SIZE_VAL, C.SHORT_SIZE_TYPE)
trading_params = TradingParams( "trading", False, True, True, 
                                99999, 
                                1.3, 1.0, "%",
                                1.3, 1.0, "%")



strategy_dataframe = last_prices.strategy



####################################################################

#   MAIN

####################################################################


# init start
# -----------------------------------------------------------

#   init and prepare dataframe
DF          = init_dataframe(paths.data_file, time_sel, delta_max="8 days", enhance_date=True)
REF_PRICES  = set_ref_prices(DF)
REF_DAYS    = set_ref_days(DF)


# save primary DF
pk_save(DF, "DF", paths.temp_path)
del DF


# graphs options
# if output.graphs : fig, axs = plt.subplots(random_sel.nb, sharex=True)
# if not isinstance(axs, Iterable) : axs = [axs,] 


# list of result
random_results = pd.Series(index=range(random_sel.nb), name="random_results", dtype=object)
random_results.index.name = "random_nb"

# -----------------------------------------------------------
# init stop



# loop start
# ------------------------------------------------------------

# main loop : for various random timestamp
for random_nb in range(random_sel.nb) : 

    # log
    # print("random_nb : ", str(random_nb))

    # df ops
    DF = pk_load("DF", paths.temp_path)
    # choose a random timestamp if needed
    if random_sel.val :   random_df = randomize_dataframe(DF, random_sel)
    else :                random_df = DF.copy()
    pk_save(random_df, "random_df", paths.temp_path)
    del random_df
    del DF

    # results
    day_results = pd.DataFrame(index=REF_DAYS, columns=REF_PRICES, dtype=object)
    day_results.index.name = "day"
    day_results.columns.name= "ref_price"

    # second loop for each day
    for day in REF_DAYS :     

        # log
        # print("\tday : ", str(day))

        # df ops
        random_df = pk_load("random_df", paths.temp_path)
        day_df = week_day_dataframe(random_df, day)  # select day df
        pk_save(day_df, "day_df", paths.temp_path)      
        del random_df
        del day_df

        # results
        ref_price_results =  pd.Series(index=REF_PRICES,  dtype=object)
        ref_price_results.index.name = "ref_price"
        
        for ref_price in REF_PRICES :   # 3rd loop for each ref prices

            
            # df ops
            day_df = pk_load("day_df", paths.temp_path)
            df = strategy_dataframe(day_df, ref_price, 3)            
            del day_df

            # update trading_params
            trading_params.price.ref = ref_price
            trading_params.update_before_trading(df)
            

            # -------------------------------------------------------------

            # trading
            df, trading_params = trading_room(df, trading_params, broker)

            # --------------------------------------------------------------

            if output.dataframes : 
                filename = ["_" + str(i) for i in [ref_price, df.date[0].day_name(), df.date.iloc[0], df.date.iloc[-1]]] 
                filename = "".join(filename).replace("-", "").replace(":", "")
                filename = "temp" + filename + ".csv"
                df.to_csv(paths.temp_path+filename, index=False)

            # compute gains
            market_start = df[ref_price].iloc[0]
            market_stop  = df[ref_price].iloc[-1]
            market_results = round((market_stop - market_start) / market_start, 2)

            trade_start = df["total"].iloc[0]
            trade_stop  = df["total"].iloc[-1]
            trade_results = round((trade_stop - trade_start) / trade_start, 2)

            ref_price_results[ref_price] = (trade_results,market_results)
#           ref_price_results[ref_price] = pd.Series(dict(trade_results=trade_results, market_results=market_results))

        day_results.loc[day, :] = ref_price_results.copy()

    random_results[random_nb] = day_results.copy()

    if output.prints :
        print("\n\n")
        print(random_nb)
        print(str(df.date.iloc[0]) + " --> " + str(df.date.iloc[-1]))
        print(day_results)
   


fig, axs = plt.subplots(4, 1, sharex= True)
_df = df.loc[:, ["date", "open", "total", "long_total", "short_total"]]               
_df.columns = ["date", "price", "portfolio", "long_total", "short_total"]                                                         

for i, txt in enumerate(["price", "portfolio", "long_total", "short_total"]) : 
    axs[i].plot("date", txt, data=_df) 
    axs[i].legend(loc="upper left")



#     if GRAPHS : 
#         axs[random_test].plot(df.date, df["total"])
#         axs[random_test].plot(df.date, df[ref_price])
#         fig.savefig(PATH + "fig")

#     meta_results.append(results_day)


# s = input("end, check/moove temps files\n's' to save\nother to delete\n\n")
# if s != "s" :  
#     master_clean(PATH)


# ------------------------------------------------------------
# loop stop


# results start
# ------------------------------------------------------------

# # results
# META_RESULTS = meta_results.copy()

# ## 1/ just take abs results
# for i, elem in enumerate(meta_results) : 
#     _df = meta_results[i]

#     for item, vect in _df.iteritems() : 
#         _df[item] = vect.apply(lambda j : j[0])


# # select main stats
# main_stats = ["mean", "50%", "25%", "75%"]
# ref_prices = [i.describe().loc[main_stats, :] for i in meta_results]
# days = [i.T.describe().loc[main_stats, :] for i in meta_results]

# # convert results in a 3d Matrix
# _ref_prices = np.array([np.array(i) for i in ref_prices])
# _days       = np.array([np.array(i) for i in days])

# # compute mean
# _ref_prices = _ref_prices.mean(axis=0)
# _days = _days.mean(axis=0)

# # return to DataFrame
# ref_prices = pd.DataFrame(_ref_prices, index=ref_prices[0].index, columns=ref_prices[0].columns)
# days = pd.DataFrame(_days, index=days[0].index, columns=days[0].columns)

# ------------------------------------------------------------
# results stop 





