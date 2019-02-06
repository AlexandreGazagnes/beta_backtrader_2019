#!/usr/bin/env python3
# coding: utf-8

####################################################################
#       CONSTANTS
####################################################################


# file and path

PATH                        = "/home/alex/beta_backtrader_2019/"
FILE                        = "dowjones_usd_abcbourse_ok.csv"
FILE                      	= "eth_usd_ethermine_ok.csv"


# ------------------------------------------------------------

# nb of last prices taken

# LAST_PRICES               = 4


# ------------------------------------------------------------

# fees and spread

FEES                        = 0.3 / 100     
# trading fees (per order)
SPREAD                      = 0.1 / 100     
# malus + or - between the price you
# ask the price you have(per order)
ROLL_OVER                   = 0.06 / 100    
# renting fees fort short (for 24h)      


# ------------------------------------------------------------

# Time selection 

TIME_SELECT                 = True

TIME_START                  = "2007-10-03"  # english format

TIME_STOP                   = "2019-01-03"

FORCE_WORKDAYS                    = False
# for real market (not crypto) delete saturdays and sundays tickers, type bool

           

# ------------------------------------------------------------

# random period and tests

RANDOMIZE                   = False         
# if you want to take a random sample of your dataset), type bool
RANDOM_NB                   = 5             
# number of random slices of the dataset, type int
RANDOM_PERIOD_MIN                  = 100           
# min perdiod of your random dataset (in days), type int
ENABLE_REVERSE              = False         
# if True 50% chance to take the random period in reverse order
# from recent to old, type bool 


# ------------------------------------------------------------

# output

GRAPHS                      = True
# print and temp save the graphs, type bool
TEMP_FILES                  = True
# print and temp save the working dataframes, type bool
PRINT_RESULTS               = True
# print and temp save the text reesults, type bool
# !!!!!!!!!!
# to code 
# !!!!!!!!!!


# ------------------------------------------------------------

# trade
VERSION                           = "trading"
# define your startegy, styp str, trading or invest
 
ENABLE_MULTI_TRADE                 = True
# if true autorise to have more than one trade open, type bool

MULTI_TRADE_MAX             = 99999
# number max of trades opened in the same time, type int

ENABLE_LONG                 = True
# enable long, type bool

ENABLE_SHORT                = False
# enable short, type bool


# ------------------------------------------------------------

# money management

LONG_BANK_INIT              = 20
# money reserved for long poisitions, type int 
# if 0 will be egaml to first df price

LONG_SIZE_VAL          = 7
# fixed size of long positions, type int

LONG_SIZE_TYPE     = "val" # or "%"
# consider POSITION_LONG_SIZE in an absolute value or in % of BANK_LONG_INIT
# type str "val" or "%"

SHORT_BANK_INIT             = 20
SHORT_SIZE_VAL         = 7
SHORT_SIZE_TYPE    = "val" # or "%"
# idem but for short



