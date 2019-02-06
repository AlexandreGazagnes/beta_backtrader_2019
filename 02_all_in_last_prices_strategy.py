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
from src.misc import *
from src.build import * 
from src.transfo import *
from src.params import * 
from src.trading import *
from src.results import * 
from strats import *


####################################################################
#       CONSTANTS
####################################################################

# paths.data_file = '/home/alex/beta_backtrader_2019/data/eth_usd_ethermine_ok.csv' # paths = Path(C.PATH, C.FILE)

time_sel = TimeSel(False, "2015-01-13", "2019-01-04") # time_sel = TimeSel(C.TIME_SELECT, C.TIME_START, C.TIME_STOP)

random_sel = RandomSel(False, 1, 400, False) # random_sel = RandomSel(C.RANDOMIZE, C.RANDOM_NB, C.RANDOM_PERIOD_MIN, C.ENABLE_REVERSE)

trading_params = TradingParams( "trading", False, True, False, # trading_params = TradingParams( C.VERSION, C.ENABLE_MULTI_TRADE, C.ENABLE_LONG, C.ENABLE_SHORT, C.MULTI_TRADE_MAX, C.LONG_BANK_INIT, C.LONG_SIZE_VAL, C.LONG_SIZE_TYPE, C.SHORT_BANK_INIT, C.SHORT_SIZE_VAL, C.SHORT_SIZE_TYPE)
                                99999, 
                                1.3, 1.0, "%",
                                1.3, 1.0, "%")


strategy_dataframe = last_prices.strategy

####################################################################

#   MAIN

####################################################################
 
t0 = time()

# init start
# -----------------------------------------------------------

#   init and prepare dataframe
DF          = init_dataframe(paths.data_file, time_sel, delta_max="8 days", enhance_date=True)
REF_PRICES  = set_ref_prices(DF)
REF_DAYS    = set_ref_days(DF)
RAND_PERIODS= set_random_dates(random_sel) 
LAST_PRICES = list(range(1, 6))


# save primary DF
pk_save(DF, "DF", paths.temp_path)
del DF


# graphs options
# if output.graphs : fig, axs = plt.subplots(random_sel.nb, sharex=True)
# if not isinstance(axs, Iterable) : axs = [axs,] 



# ------------------------------------------------------------

# main loop : for various random timestamp
for random_nb in range(random_sel.nb) : 

    # df ops
    DF = pk_load("DF", paths.temp_path)
    # choose a random timestamp if needed
    if random_sel.val :   random_df = randomize_dataframe(DF, random_sel)
    else :                random_df = DF.copy()
    del DF

    # results
    axis_struct = (("rand_periods", RAND_PERIODS) "last_prices", LAST_PRICES), ("ref_days", REF_DAYS), ("ref_prices", REF_PRICES)) 
    data_label = ("trd", "mkt")
    r = Results(axis_struct, data_label, ("start", "stop"))

    # main loop
    LOOPER = [[(j,k) for j,k in enumerate(i)] for i in [RAND_PERIODS, LAST_PRICES, REF_DAYS , REF_PRICES]]
    for period, param, day, ref_price in product(*LOOPER) : 

        # unpack enumerate results
        h, period = period
        i, param = param
        j, day = day
        k, ref_price = ref_price
        print(param,day,ref_price)

        # update df
        df      = week_day_dataframe(random_df.copy(), day)
        df      = strategy_dataframe(df, ref_price, param)            

        # update trading_params
        trading_params.price.ref = ref_price
        trading_params.update_before_trading(df)
        
        # trading
        df, trading_params = trading_room(df, trading_params, broker)

        # save temp_df if needed
        if output.dataframes : 
            save_temp_df(df, [param, day, ref_price], paths.temp_path)


        # compute gains

        rs = compute_trading_results(df, ref_price)
        print(f"\t{rs}\n")
        r.m[i, j, k] = rs

    random_results[random_nb] = None

    # # show results
    # if output.prints :
    #     print("\n\n")
    #     print(random_nb)
    #     print(str(df.date.iloc[0]) + " --> " + str(df.date.iloc[-1]))
    #     print(day_results)
       

# time
timer = round(time() - t0,4)
print(str(timer))

# graph
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





