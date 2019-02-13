#!/usr/bin/env python3
# coding: utf-8



####################################################################
#       test_rolling_fees
####################################################################



####################################################################
#       IMPORT
####################################################################

# built-in
import os, sys, datetime, time, pickle
from collections import Iterable
from copy import copy
from time import gmtime, strftime, time
from itertools import product
from multiprocessing import Process
from logging import warning

# visualizitation
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib
sns.set()

# src
path = os.getcwd()
path = path.split("/")
path = path[:-1]
path = "/".join(path) + "/"
os.chdir(path)

from src.misc       import *
from src.build      import * 
from src.transfo    import *
from src.params     import * 
from src.trading    import *
from src.results    import * 
from strats         import *


####################################################################
#       CONSTANTS
####################################################################

paths.data_file     = '/home/alex/beta_backtrader_2019/tests/test_rolling_fees.csv'
broker              = Broker(C.FEES, C.SPREAD, 0.00000001)
time_sel            = TimeSel(False, "2006-01-01", "2020-01-01")
random_sel          = RandomSel(False, 10, 100,  10*360, False)
trading_params      = TradingParams(    "trading", False, 99999, 
                                        False, True, 
                                        False, 100,
                                        1.0, "%",
                                        1.0, "%")
multi_process       = MultiProcessing(False, 6)
strategy_dataframe  = last_prices.strategy



####################################################################
#   INIT
####################################################################

# time it 
t0 = time()

#   init and prepare dataframe
DF                  = init_dataframe(paths.data_file, time_sel, trading_params)
pk_save(DF, "DF", paths.temp_path_dfs)

# init our LOOPER
REF_PRICES          = ["open"]                # ["open", "close", "average", "clos_op"]
REF_DAYS            = [0,]                  # [0, 1, 2, 3, 4]
RAND_PERIODS        = set_rand_periods(DF, random_sel)  # list of random (timestamp_start, timestamp_stop)
LAST_PRICES         = [2,]                
LOOPER              = [i for i in product(RAND_PERIODS, LAST_PRICES, REF_DAYS , REF_PRICES)]

# init result handler
axis_struct         = ("rand_periods", "last_prices", "ref_days", "ref_prices")
data_label          = ("trd", "mkt", "time")
start_stop          = (str(DF.iloc[0]["date"]), str(DF.iloc[-1]["date"]))
results             = Results(axis_struct, data_label, start_stop, paths.data_file)

# timer
timer = round(time() - t0, 4)
print("timer init : ", str(timer))
t1 = time()


####################################################################
#   TRADING
####################################################################


def back_trade(looper_start=-1, looper_stop=-1) :
    
    # args check
    assert isinstance(looper_start, int)
    assert isinstance(looper_stop, int)
    if looper_start <0 : looper_start = 0
    if looper_stop  <0 : looper_stop  = len(LOOPER)+1

    # main loop
    for period, param, day, ref_price in LOOPER[looper_start : looper_stop] : 

        trd_params      = trading_params.copy()
        t_loop          = time()

        # update df
        df              = DF.copy()
        df              = random_dataframe(df, period) 
        df              = week_day_dataframe(df, day)
        df              = strategy_dataframe(df, trd_params, param)            

        # update trading_params and trading
        trd_params.update_before_trading(df, ref_price)
        df, trd_params  = trading_room(df, trd_params, broker)

        # compute gains and upadate results
        rs              = compute_trading_results(df, ref_price)
        ser             = ( time_to_float_period(period), param, day, ref_price, 
                            round(rs[0], 2), round(rs[1], 2), round(time() - t_loop, 2))
        # r.m.append(ser)

        # save results
        filename        = "_".join([str(i) for i in (time_to_float_period(period), param, day, ref_price)])      
        pk_save(ser, filename, paths.temp_path_results) # print(filename)

        # prints and temp
        if output.prints :     print("\t".join([str(i) for i in ser]))
        if output.dataframes : save_temp_df(df, filename, paths.temp_path_dfs)



####################################################################
#   PROCESS
####################################################################


# multiprocessing
if not multi_process.val : 
    back_trade()
else : 
    chks  = chunks(LOOPER, multi_process.nb_cores)
    process_list = [Process(target=back_trade, args=chk) for chk in chks]
    [i.start() for i in process_list]
    [i.join()  for i in process_list]

# timer
timer = round(time() - t1, 4)
print("timer process : ", str(timer))
timer = round(time() - t0, 4)
print("timer global : ", str(timer))
