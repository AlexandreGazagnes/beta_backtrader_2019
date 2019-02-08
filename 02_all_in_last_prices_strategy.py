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
from time import gmtime, strftime, time
from itertools import product


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

# paths.data_file = '/home/alex/beta_backtrader_2019/data/eth_usd_ethermine_ok.csv' # paths = Path(C.PATH, C.FILE)

time_sel        = TimeSel(True, "1999-01-13", "2022-11-04") # time_sel = TimeSel(C.TIME_SELECT, C.TIME_START, C.TIME_STOP)

random_sel      = RandomSel(True, 5, 400, False) # random_sel = RandomSel(C.RANDOMIZE, C.RANDOM_NB, C.RANDOM_PERIOD_MIN, C.ENABLE_REVERSE)

trading_params  = TradingParams( "trading", False, True, False, # trading_params = TradingParams( C.VERSION, C.ENABLE_MULTI_TRADE, C.ENABLE_LONG, C.ENABLE_SHORT, C.MULTI_TRADE_MAX, C.LONG_BANK_INIT, C.LONG_SIZE_VAL, C.LONG_SIZE_TYPE, C.SHORT_BANK_INIT, C.SHORT_SIZE_VAL, C.SHORT_SIZE_TYPE)
                                99999, 
                                1.3, 1.0, "%",
                                1.3, 1.0, "%")

strategy_dataframe = last_prices.strategy



####################################################################
#   MAIN
####################################################################
 
# init start
# -----------------------------------------------------------

# time it 
t0 = time()


#   init and prepare dataframe
DF              = init_dataframe(paths.data_file, time_sel, enhance_date=True)
pk_save(DF, "DF", paths.temp_path)


# init our LOOPER
REF_PRICES      = set_ref_prices(DF)
REF_DAYS        = set_ref_days(DF)
RAND_PERIODS    = set_rand_periods(DF, random_sel) 
LAST_PRICES     = list(range(1, 6))
LOOPER          = [i for i in product(RAND_PERIODS, LAST_PRICES, REF_DAYS , REF_PRICES)]

# init result handler
axis_struct     = ("rand_periods", "last_prices", "ref_days", "ref_prices")
data_label      = ("trd", "mkt")
start_stop      = (str(DF.iloc[0]["date"]), str(DF.iloc[-1]["date"]))
r = Results(axis_struct, data_label, start_stop)


# init graphs options
# if output.graphs : fig, axs = plt.subplots(random_sel.nb, sharex=True)
# if not isinstance(axs, Iterable) : axs = [axs,] 

# -----------------------------------------------------------
# init stop


# loop strat
# -----------------------------------------------------------

for period, param, day, ref_price in LOOPER : 

    # unpack enumerate results
    # h, period       = period
    # i, param        = param
    # j, day          = day
    # k, ref_price    = ref_price
    # print(str_timestamp(period[0]), str_timestamp(period[1]), param, day, ref_price)

    # update df
    df      = DF.copy()
    df      = random_dataframe(df, period) 
    df      = week_day_dataframe(df, day)
    df      = strategy_dataframe(df, ref_price, param)            


    # update trading_params
    trading_params.update_before_trading(df, ref_price)
    df, trading_params = trading_room(df, trading_params, broker)


    # save temp_df if needed
    if output.dataframes : save_temp_df(df, [param, ref_price], paths.temp_path)


    # compute gains and upadate results
    rs = compute_trading_results(df, ref_price)

    ser = (float_period(period), param, day, ref_price, rs[0], rs[1])
    r.m.append(ser)


    # show results
    if output.prints :
        print(str(float_period(period)), param, day, ref_price, rs)
        # print(f"\t{rs}\n")


    # grah results:
    #     axs[random_test].plot(df.date, df["total"])
    #     axs[random_test].plot(df.date, df[ref_price])
    #     fig.savefig(PATH + "fig")


# -----------------------------------------------------------
# stop strat       



# post prod strat
# -----------------------------------------------------------

# time it 
timer = round(time() - t0,4)
print(str(timer))


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

