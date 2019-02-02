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



####################################################################
#       CONSTANTS
####################################################################


# file path
PATH            = "/home/alex/Downloads/ABC_bourse/"
FILE            = "DJIA_20_years.csv"
FILE            = "export-EtherPrice.csv"


# nb of last prices taken
LAST_PRICES     = 4


# fees and spread
FEES            = 0.3 / 100
SPREAD          = 0.1 / 100 


# random period and tests
RANDOMIZE           = True 
RANDOM_NB           = 5
if not RANDOMIZE : RANDOM_NB = 1
PERIOD_MIN          = 100           # in DAYS !!!!
ENABLE_REVERSE      = False         # NOT IMPLEMENTED


# bank
BANK_INIT = 0


# days 
WORKDAYS = False


# output
GRAPHS          = True
TEMP_FILES      = True
PRINT_RESULTS   = True


# Time selection 
TIME_SELECT = False
TIME_START = "2017-05-03"
TIME_STOP  = "2019-01-03"


####################################################################

# Join and merge various same file of differnet timestamp
"""

files = os.listdir(PATH)
files = sorted([i for i in files if ".csv" in i], reverse=True)


dfs = [pd.read_csv(PATH + i, sep=";", decimal=",", header=None) for i in files]
df = pd.concat(dfs, axis=0, ignore_index=True)    


del dfs

cols = ["id", "date", "open", "high", "low", "close", "vol"]
df.columns = cols
df.drop(["id", "vol"], axis=1, inplace=True)
df["date"] = pd.to_datetime(df.date, dayfirst=True)
df["day"] = df.date.apply(lambda i : i.day_name())


plt.plot(df.date, df.open)
plt.show()


days = df.day.unique()
saturdays = df.loc[df.day == "Saturday" , :].index 
sundays = df.loc[df.day == "Sunday" , :].index   


flatten = lambda l: [item for sublist in l for item in sublist]
df.drop(flatten([saturdays, sundays]), axis=0, inplace=True)
del saturdays, sundays
days = df.day.unique()

df.index = range(len(df.index))

df.to_csv("/home/alex/Downloads/ABC_bourse/") 
"""

####################################################################



####################################################################
#       FUNCTIONS
####################################################################


# misc. functions
# -----------------------------------------------------------

def pk_save(data, filename, path) : 

    filename = str(path+filename+".pk")
    with open(filename, 'wb') as f :
        pk = pickle.Pickler(f)
        pk.dump(data)


def pk_load(filename, path) : 

    filename = str(path+filename+".pk")
    with open(filename, 'rb') as f :
        pk = pickle.Unpickler(f)
        return pk .load()


def _clean(path, ext) : 

    files = [f for f in os.listdir(PATH) if os.path.isfile(PATH + f)]
    _ = [os.remove(path+i) for i in files if ext in i]


def pk_clean(path) : 
 
    _clean(path, ".pk")


def temp_clean(path) : 
    
    _clean(path, "temp")


def graph_clean(path) : 
    
    _clean(path, ".png")


def master_clean(path) : 

    pk_clean(PATH)
    temp_clean(PATH)
    graph_clean(PATH)


# init functions
# -----------------------------------------------------------

def init_dataframe(path, file) : 
    # check path dand file integrity
    if path[-1] != "/" : path +="/"
    code = """
    list dir in path
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"""

    # init df
    df = pd.read_csv(path+file)
    df.columns = [i.lower() for i in df.columns]
    if "date" not in df.columns : 
        raise ValueError("please be sure to have a date column")

    # check decimal integrity
    cols = df.columns.drop("date")
    for col in cols : 
        try :       pd.to_numeric(df[col])
        except :    raise TypeError("non numeric columns, convert ',' to '.' ")

    return df


def check_OHLC_format(df) : 

    if (        (not "open" in df.columns)  or (not "close" in df.columns)
            or  (not "high" in df.columns)  or (not "low" in df.columns)    )  : 

            print("\n\ndataframe columns are : {}".format(df.columns))
            k = input("OHLC format invalid please entre 'f' to force program, other key to stop\n\n")
            if k != "f" : raise KeyboardInterrupt("user choose to quit program")


def average_and_close_open(df, average=True, close_open=True) :  

    # add close_open
    if close_open and (("open" and "close") in df.columns) and ("close_open" not in df.columns) : 
        df["close_open"] = (df["open"] + df["close"]) / 2

    # add average
    if average and (("open" and "high" and "low" and "close") in df.columns) and ("average" not in df.columns) : 
        df["average"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4

    return df 


def convert_date(df) : 
    
    # convert date format
    df["date"] = pd.to_datetime(df.date)
    
    # check date integrity
    code = """
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"""

    return df


def set_ref_prices(df) : 

    # remember prices columns
    ref_prices = df.columns.drop("date")
    
    if ("week_day" or "month" or "year") in ref_prices : 
        raise ValueError("no day, month or year in ref_prices")

    for i in ["high", "low"] : 
        if i in ref_prices : ref_prices = ref_prices.drop(i)

    return ref_prices


def enhance_date(df, year_lim=1985, week_day=True, month_day=True, month=True, year=True) :

    # handle days of week and month
    if week_day and not ("week_day" in df.columns) : 
        df["week_day"] = df.date.apply(lambda i : i.dayofweek)
    if month_day and not ("month_day" in df.columns) : 
        df["month_day"] = df.date.apply(lambda i : i.day)
    if month and not ("month" in df.columns) : 
        df["month"] = df.date.apply(lambda i : i.month) 
    if year and not ("year" in df.columns) : 
        df["year"] = df.date.apply(lambda i : i.year)

    # check date integrity
    for y in df.year.unique() : 
        if (y < year_lim) or (y >  int(datetime.date.today().year)) :  
            raise ValueError("Date Error : {}".format())

    return df


def set_days(df) : 
    
    # remember days
    if not "week_day" in df.columns : 
        raise ValueError("no wek_day in columns")

    days = sorted(df.week_day.unique()) 
    
    return days


def force_wordays(df) : 

    # force workdays if needed (crypto vs classic market)
    if not "week_day" in df.columns : 
        raise ValueError("no wek_day in columns")

    idxs = df.loc[df["week_day"] > 4, :].index
    df.drop(idxs, axis=0, inplace=True)
    df.index = list(range(len(df.index)))

    return df


def time_selection(df, start, stop) : 

    # time selection if needed
    start = pd.to_datetime(start) 
    stop = pd.to_datetime(stop)
    
    start = df.loc[df.date == start, :].index
    stop  = df.loc[df.date == stop, :].index

    if len(start) != 1 : raise ValueError("time start not  good") 
    if len(stop)  != 1 : raise ValueError("time stop not  good") 

    df = df.loc[start[0] : stop[0], :].copy()
    df.index = list(range(len(df.index)))   

    return df


def build_dataframe(path, file, workdays, time_select, start, stop) : 

    df = init_dataframe(path, file)

    check_OHLC_format(df)
    df = average_and_close_open(df)
    df = convert_date(df)

    ref_prices = set_ref_prices(df)
    
    df = enhance_date(df)
    
    days = set_days(df)

    if workdays :               df = force_wordays(df)
    if time_select :         df = time_selection(df, start, stop)

    return df, ref_prices, days


# dataframe preparation functions
# -----------------------------------------------------------

def random_dataframe(df, period_min, enable_reverse) : 

    _df = df.copy()
    
    while True : 
        start = np.random.randint(0, len(_df.index)-1)   
        stop  = np.random.randint(start+1, len(_df.index))
        if (stop - start) > period_min : break
    
    # update random_df
    _df = _df.iloc[start : stop, :].copy()
    _df.index = list(range(len(_df.index))) 

    if enable_reverse and np.random.randint(0,2) : 
        raise ValueError("not implemeted")
        code = """
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        """
    _df.index = list(range(len(_df.index)))

    return _df


def day_dataframe(df, day) : 
    
    _df = df.copy()

    # select day and reindex df
    _df = df.loc[df["week_day"] == day, :].copy()
    _df.index = list(range(len(_df.index)))

    return _df


def last_prices_dataframe(df, ref_price, last_prices) : 

    _df = df.copy()

    # build last prices
    for i in range(1, 1+last_prices) : 
        _df["last_"+str(i)+"_week"] = round(100 *  (_df[ref_price] - _df[ref_price].shift(i)) / _df[ref_price].shift(i),2)

    # build primary indicators
    cols =  [ i for i in _df.columns if "last" in i]
    _df["all_green"]    = (_df.loc[:, cols] > 0).all(axis = 1)
    _df["all_red"]      = (_df.loc[:, cols] < 0).all(axis = 1)
    _df["indicator"]        = 0
    _df.loc[_df["all_green"] == True , "indicator"] = 2
    _df.loc[_df["last_1_week"] < 0, "indicator"]    = -1
    _df.loc[_df["all_red"] == True, "indicator"]    = -2


    # drop ligns without indicators
    _df = _df.iloc[last_prices:, :].copy()
    _df.index = list(range(len(_df.index)))

    return _df


# trading functions
# -----------------------------------------------------------

def trading_dataframe(df) : 

    _df = df.copy()

    # init trading columns
    _df["bank"]  = 0.0
    _df["value"] = 0.0
    _df["quant"] = 0.0

    _df.index = list(range(len(_df.index)))

    return _df


def set_trading_params(df, ref_price, bank_init) : 

    # for average and close_open you have to buy at close
    if  ref_price in ["average", "close_open"] :    _ref_price = "close"
    elif ref_price in ["high", "low"] :             raise ValueError("invalid ref_price")
    else :                                          _ref_price = ref_price

    # update bank init as required
    if not bank_init : bank = df[_ref_price].iloc[0]
    else :             bank = bank_init

    # dumb vars
    trade_open  = False
    last_buy    = -1
    first       = True

    return _ref_price, bank, trade_open, last_buy, first


def do_nothing(df, i, _ref_price) : 
    
    _df = df.copy()
    _df.loc[i, "bank"]  = _df.loc[i-1, "bank"]
    _df.loc[i, "quant"] = _df.loc[i-1, "quant"]  
    _df.loc[i, "value"] = _df.loc[i-1, "quant"] * _df.loc[i, _ref_price]

    return _df 
    

def long_buy(df, i, trade_open, last_buy, _ref_price, spread, fees) : 

    if not trade_open : 
        _df = df.copy()
        bank = _df.loc[i-1, "bank"]
        price = _df.loc[i, _ref_price]
        _df.loc[i, "bank"] = 0
        quant = bank * (1 - spread) * (1 - fees) / price
        _df.loc[i, "quant"] = quant
        _df.loc[i, "value"] = quant * price
        last_buy = price
        trade_open=True
    
    else : 
        _df = do_nothing(df, i, _ref_price)

    return _df, trade_open, last_buy


def long_stop_profit(df, i, trade_open, last_buy, _ref_price, spread, fees) : 

    if  trade_open : 
        _df = df.copy()
        quant = _df.loc[i-1, "quant"]
        price = _df.loc[i, _ref_price]
        _df.loc[i, "quant"] = 0
        bank = quant * price
        _df.loc[i, "quant"] = 0
        _df.loc[i, "value"] = 0
        _df.loc[i, "bank"] = bank * (1 - spread) * (1 - fees)
        last_buy = -1
        trade_open=False
    
    else : 
        _df = do_nothing(df, i, _ref_price)

    return _df, trade_open, last_buy


def long_stop_loss(df, i, trade_open, last_buy, _ref_price, spread, fees) : 

    if trade_open and (last_buy > df.loc[i, _ref_price]): 
        _df = df.copy()
        quant = _df.loc[i-1, "quant"]
        price = _df.loc[i, _ref_price]
        _df.loc[i, "quant"] = 0
        bank = quant * price
        _df.loc[i, "quant"] = 0
        _df.loc[i, "value"] = 0
        _df.loc[i, "bank"] = bank * (1 - spread) * (1 - fees)
        last_buy = -1
        trade_open=False
    
    else : 
        _df = do_nothing(df, i, _ref_price)

    return _df, trade_open, last_buy



####################################################################

#   MAIN

####################################################################


# init start
# -----------------------------------------------------------

#   init and prepare dataframe
DF, REF_PRICES, DAYS = build_dataframe(PATH, FILE, WORKDAYS, TIME_SELECT, TIME_START, TIME_STOP)

pk_save(DF, "DF", PATH)
del DF

#  handle main loop if not randomize period - > just one loop 
if GRAPHS : fig, axs = plt.subplots(RANDOM_NB, sharex=True)
if not isinstance(axs, Iterable) : axs = [axs,] 


# list of result
meta_results = list()

# -----------------------------------------------------------
# init stop



# loop start
# ------------------------------------------------------------

for random_test in range(RANDOM_NB) : # main loop : for various random timestamp

    DF = pk_load("DF", PATH)

    # choose a random timestamp if needed
    if RANDOMIZE :  random_df = random_dataframe(DF, PERIOD_MIN, ENABLE_REVERSE)
    else :          random_df = DF.copy()

    pk_save(random_df, "random_df", PATH)
    del random_df
    del DF

    results_day = pd.DataFrame(columns=REF_PRICES) # prepare results


    for day in DAYS :     # second loop for each day

        random_df = pk_load("random_df", PATH)

        day_df = day_dataframe(random_df, day)  # select day df

        pk_save(day_df, "day_df", PATH)      
        del random_df
        del day_df

        results_ref_price = list()         # results

        for ref_price in REF_PRICES :   # 3rd loop for each ref prices

            day_df = pk_load("day_df", PATH)
            df = last_prices_dataframe(day_df, ref_price, LAST_PRICES)
            
            del day_df

            # trading start
            # ---------------------------------------------------------

            df = trading_dataframe(df)

            _ref_price, bank_init, trade_open, last_buy, first = \
                        set_trading_params(df, ref_price, BANK_INIT)

            for _, i in enumerate(df.index) : # trading loop

                if first:  # first
                    df.loc[i, "bank"], first = bank_init, False
                    continue

                if df.loc[i, "indicator"] == 2 : # buy
                    df, trade_open, last_buy = long_buy(
                        df,i,trade_open,last_buy,_ref_price,SPREAD,FEES)

                elif df.loc[i, "indicator"] == -2 : # stop profit
                    df, trade_open, last_buy = long_stop_profit(
                        df,i,trade_open,last_buy,_ref_price,SPREAD,FEES)

                elif df.loc[i, "indicator"] == -1 :  # stop loss
                    df, trade_open, last_buy = long_stop_loss(
                        df,i,trade_open,last_buy,_ref_price,SPREAD,FEES)

                else : # do nothing
                    df = do_nothing(df, i, _ref_price)

            df["total"] = df.bank + df.value

            # ---------------------------------------------------------
            # trading stop


            # compute gains
            market_start = df[_ref_price].iloc[0]
            market_stop  = df[_ref_price].iloc[-1]
            market_results = round(100 * (market_stop - market_start) / market_start, 2)

            trade_start = df["total"].iloc[0]
            trade_stop  = df["total"].iloc[-1]
            trade_results = round(100 * (trade_stop - trade_start) / trade_start, 2)


            # update 2nd level results
            results_ref_price.append((trade_results, market_results)) 
            # add len(df.index) to be able to know if corr with le len of the period


        # update 1st level results
        results_ref_price = pd.Series(results_ref_price, index=REF_PRICES, name=day)
        results_day = results_day.append(results_ref_price)


    if PRINT_RESULTS :
        print("\n\n")
        print(random_test)
        print(day)
        print(ref_price)
        print(_ref_price)
        print(df.shape)
        print(df.date.head())
        print(df.date.tail())
        print(df.columns)
        print(results_day)
   

    if TEMP_FILES : 
        filename = ["_" + str(i) for i in [ref_price, df.date[0].day_name(), df.date.iloc[0], df.date.iloc[-1]]] 
        filename = "".join(filename).replace("-", "").replace(":", "")
        filename = "temp" + filename + ".csv"
        df.to_csv(PATH+filename, index=False)


    if GRAPHS : 
        axs[random_test].plot(df.date, df["total"])
        axs[random_test].plot(df.date, df[ref_price])
        fig.savefig(PATH + "fig")

    meta_results.append(results_day)


s = input("end, check/moove temps files\n's' to save\nother to delete\n\n")
if s != "s" :  
    master_clean(PATH)


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



