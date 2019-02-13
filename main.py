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


# paths.data_file   = '/home/alex/beta_backtrader_2019/data/eth_usd_ethermine_ok.csv' # paths = Path(C.PATH, C.FILE)

time_sel            = TimeSel(False, "2006-01-01", "2020-01-01") # time_sel = TimeSel(C.TIME_SELECT, C.TIME_START, C.TIME_STOP)

random_sel          = RandomSel(False, 10, 100,  10*360, False) # random_sel = RandomSel(C.RANDOMIZE, C.RANDOM_NB, C.RANDOM_PERIOD_MIN, C.RANDOM_PERIOD_MAX, C.ENABLE_REVERSE)

trading_params      = TradingParams(    "trading", False, 99999, 
                                        True, True, 
                                        False, 100, # trading_params = TradingParams( C.VERSION, C.ENABLE_MULTI_TRADE, C.ENABLE_LONG, C.ENABLE_SHORT, C.DUAL_BANK, C.MULTI_TRADE_MAX, C.LONG_BANK_INIT, C.LONG_SIZE_VAL, C.LONG_SIZE_TYPE, C.SHORT_BANK_INIT, C.SHORT_SIZE_VAL, C.SHORT_SIZE_TYPE)
                                        1.0, "%",
                                        1.0, "%")

multi_process       = MultiProcessing(True, 6)    # multi_process = MultiProcessing(C.ENABLE_MULTI_PROCESSING, C.NB_CORES)

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
REF_PRICES          = set_ref_prices(DF)                # ["open", "close", "average", "clos_op"]
REF_DAYS            = set_ref_days(DF)                  # [0, 1, 2, 3, 4]
RAND_PERIODS        = set_rand_periods(DF, random_sel)  # list of random (timestamp_start, timestamp_stop)
LAST_PRICES         = list(range(1, 7))                 
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


def trading(looper_start=-1, looper_stop=-1) :
    
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
        ser             = (time_to_float_period(period), param, day, ref_price, rs[0], rs[1], round(time() - t_loop, 4))
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
    trading()
else : 
    chks  = chunks(LOOPER, multi_process.nb_cores)
    process_list = [Process(target=trading, args=chk) for chk in chks]
    [i.start() for i in process_list]
    [i.join()  for i in process_list]

# timer
timer = round(time() - t1, 4)
print("timer process : ", str(timer))
timer = round(time() - t0, 4)
print("timer global : ", str(timer))



####################################################################
#   RESULTS
####################################################################


# load
results.load(paths)
# print(r.m.groupby(by="last_prices").mean())

# graph
files = [i for i in os.listdir(paths.temp_path_dfs) if ".csv" in i] 
print(files[0])
df = pd.read_csv(paths.temp_path_dfs + files[0]) 
cols = [i for i in df.columns if "total" in i] + ["open"]
df.set_index("date", inplace=True, drop=True)
df.index = map(lambda i : pd.Timestamp(i), df.index)
df.drop([i for i in df.columns if i not in cols], axis=1, inplace=True)
df.plot()



####################################################################
#   TRASH
####################################################################


# grah results:
#     axs[random_test].plot(df.date, df["total"])
#     axs[random_test].plot(df.date, df[ref_price])
#     fig.savefig(PATH + "fig")


# init graphs options
# if output.graphs : fig, axs = plt.subplots(random_sel.nb, sharex=True)
# if not isinstance(axs, Iterable) : axs = [axs,] 


# # graph last df 
# fig, axs = plt.subplots(4, 1, sharex= True)
# _df = df.loc[:, ["date", "open", "total", "long_total", "short_total"]]               
# _df.columns = ["date", "price", "portfolio", "long_total", "short_total"]                                                         

# for i, txt in enumerate(["price", "portfolio", "long_total", "short_total"]) : 
#     axs[i].plot("date", txt, data=_df) 
#     axs[i].legend(loc="upper left")


# # clean temp if needed
# s = input("end, check/moove temps files\n's' to save\nother to delete\n\n")
# if s != "s" :  
#     master_clean(paths.temp_path)


