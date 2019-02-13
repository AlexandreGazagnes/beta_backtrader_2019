#!/usr/bin/env python3
# coding: utf-8


# multi processing
# ------------------------------------------------------------

ENABLE_MULTI_PROCESSING             = True
NB_CORES                            = 6


# file and path
# ------------------------------------------------------------

PATH                                = "/home/alex/beta_backtrader_2019/"
FILE                                = "dowjones_usd_abcbourse_ok.csv"
FILE                                = "eth_usd_ethermine_ok.csv"
FILE                                = "test2.csv"


# fees and spread
# ------------------------------------------------------------

FEES                                = 0.3 / 100     
# trading fees (per order)
SPREAD                              = 0.1 / 100     
# malus + or - between the price you
# ask the price you have(per order)
ROLL_OVER                           = 0.06 / 100
ROLL_OVER                           = 1 / 100
# renting fees fort short (for 24h)      



# Time selection 
# ------------------------------------------------------------

TIME_SELECT                         = True
TIME_START                          = "2017-10-03"  # english format
TIME_STOP                           = "2018-11-04"
FORCE_WORKDAYS                      = False
# for real market (not crypto) delete saturdays and sundays tickers, type bool
           


# random periods
# ------------------------------------------------------------

RANDOMIZE                           = False         
# if you want to take a random sample of your dataset), type bool
RANDOM_NB                           = 5             
# number of random slices of the dataset, type int
RANDOM_PERIOD_MIN                   = 100           
RANDOM_PERIOD_MAX                   = 3600
# min perdiod of your random dataset (in days), type int
ENABLE_REVERSE                      = False         
# if True 50% chance to take the random period in reverse order
# from recent to old, type bool 



# outputs
# ------------------------------------------------------------

GRAPHS                              = True
# print and temp save the graphs, type bool
TEMP_FILES                          = True
# print and temp save the working dataframes, type bool
PRINT_RESULTS                       = True
# print and temp save the text reesults, type bool
# !!!!!!!!!!
# to code 
# !!!!!!!!!!



# trading main features
# ------------------------------------------------------------

VERSION                             = "trading"
# define your startegy, styp str, trading or invest
 
ENABLE_MULTI_TRADE                  = True
# if true autorise to have more than one trade open, type bool

MULTI_TRADE_MAX                     = 99999
# number max of trades opened in the same time, type int

ENABLE_LONG                         = True
# enable long, type bool

ENABLE_SHORT                        = False
# enable short, type bool

DUAL_BANK                           = True
BANK_INIT                           = -1
# 


# money management
# ------------------------------------------------------------


LONG_SIZE_VAL                       = 7
# fixed size of long positions, type int

LONG_SIZE_TYPE                      = "val" # or "%"
# consider POSITION_LONG_SIZE in an absolute value or in % of BANK_LONG_INIT
# type str "val" or "%"

SHORT_SIZE_VAL                      = 7
SHORT_SIZE_TYPE                     = "val" # or "%"
# idem but for short



