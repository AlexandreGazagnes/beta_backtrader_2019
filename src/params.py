#!/usr/bin/env python3
# coding: utf-8



# built-in
import os
import pandas as pd

# 3rd party
from config.consts import *



# params
# -----------------------------------------------------------
class MultiProcessing() : 

    def __init__(self, val, nb_cores) : 

        # check args
        assert isinstance(val, bool)
        assert isinstance(nb_cores, int)
        assert ((nb_cores>0) and (nb_cores<=6))

        self.val = val
        self.nb_cores = nb_cores

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")


class Path() : 

    def __init__(self, path, filename) : 

        # check args
        if path[-1] != "/" : path += "/"

        for fol in ['data', "results", "temp"] : 
            if not os.path.isdir(path+fol+"/") : 
                os.mkdir(path+fol+"/")

        assert os.path.isdir(path)
        self.master_path = path
       
        assert os.path.isdir(path+"data/")
        self.data_path = path+"data/"

        assert os.path.isfile(path+"data/"+filename)
        self.data_file = path+"data/"+filename

        assert os.path.isdir(path+"results/")
        self.results_path = path+"results/"

        assert os.path.isdir(path+"temp/")
        self.temp_path = path+"temp/"

        for fol in ["results", "dfs"] : 
            if not os.path.isdir(path+"temp/"+fol+"/") : 
                os.mkdir(path+"temp/"+fol+"/")

        self.temp_path_results  = self.temp_path+"results/"
        self.temp_path_dfs      = self.temp_path+"dfs/"

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")


class Broker() : 

    def __init__(self, fees=0.003, spread=0.001, roll_over=0.00006) : 
        
        # check args
        for i in [fees, spread, roll_over] : 
            assert isinstance(i, float)
            assert ((i >0.0) and (i < 0.05))

        self.fees           = fees
        self.spread         = spread
        self.roll_over      = roll_over

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")

  
class TimeSel() : 
    
    def __init__(self, val, start=None, stop=None, delta_max="8 days", force_workdays=False, ) : 

        # check args
        assert isinstance(val, bool)
        assert isinstance(force_workdays, bool)  

        if val : 
            for d in [start, stop] : 
                d = [int(d) for d in d.split("-")]
                assert ((d[0] >= 1980)  and (d[0] <=2025))
                assert ((d[1] >= 1)     and (d[1] <=12))
                assert ((d[2] >= 1)     and (d[2] <=31))

        assert pd.to_datetime(stop) > pd.to_datetime(start)

        self.val            = val
        
        if val : 
            self.start          = start
            self.stop           = stop
            self.force_workdays = force_workdays
            self.delta_max      = delta_max
        
        else : 
            self.start          = None
            self.stop           = None
            self.force_workdays = False
            self.delta_max      = delta_max

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")


class RandomSel() : 

    def __init__(self, val, nb=0, period_min=360, period_max=3600,reverse=False) : 
        
        # check args
        assert isinstance(val, bool)         

        if val : 
            assert isinstance(nb, int)
            assert ((nb >= 1) and (100 >= nb))             
            assert isinstance(period_min, int)
            assert ((period_min >= 10) and (365*30 >= period_min))                 
            assert isinstance(reverse, bool)

        self.val = val
        
        if val : 
            self.nb         = nb
            self.period_min       = period_min
            self.period_max       = period_max
            self.reverse    = reverse
        
        else :    
            self.nb         = 1
            self.period_min = None
            self.period_max       = period_max
            self.reverse    = None        

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")


class Output() : 

    def __init__(self, graphs=True, dataframes=True, prints=True, path=None) : 

        # check agrs
        for i in [graphs, dataframes, prints] : 
            assert isinstance(i, bool)

        if graphs or dataframes or prints : 
            assert os.path.isdir(path)

        self.graphs     = graphs
        self.dataframes = dataframes
        self.prints     = prints
        self.path       = path

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")


class Bank() : 

    def __init__(self, dual=True, init=-1) : 

        assert isinstance(dual, bool)
        assert (isinstance(init, int) or isinstance(init, float))
        assert ((init>= -1) and (init <= 10000))

        self.dual   = dual
        
        if dual : 
            self.long_init  = round(init/2, 4)
            self.short_init = round(init/2, 4)

        else : 
            self.init       = init
    
    def __repr__(self) : 

        return str(self.__dict__).replace(",", ";\n").replace(":", "=")


class MultiTrade(): 

    def __init__(self, version, enable, multi_trade_max=999999) : 

        # args check         
        assert isinstance(version, str)
        assert (version.lower() in ["invest", "trading"])

        assert isinstance(enable, bool)
        if enable :   
            assert isinstance(multi_trade_max, int)  
            assert ((multi_trade_max >= 1) and (999999 >= multi_trade_max))         

        self.version            = version.lower()
        self.enable             = enable
        self.multi_trade_max    = multi_trade_max


    def __repr__(self) : 

        return str(self.__dict__).replace(",", ";\n").replace(":", "=")


class Price() : 

    def __init__(self) : 
        self._ref = "open"
        self._mkt = "open"

    def __get_ref(self) : 
        return self._ref

    def __get_mkt(self) : 
        return self._mkt

    def __set_ref(self, val) : 
        assert isinstance(val, str)
        assert val in ("open", "close", "clos_op", "average")
        self._ref = val

    def __set_mkt(self, val) : 
        assert isinstance(val, str)
        assert val in ("open", "close")
        self._mkt = val

    ref         = property(__get_ref, __set_ref)
    mkt         = property(__get_mkt, __set_mkt)

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ";\n").replace(":", "=")



class Position() : 

    def __init__(self, enable, size_val=None, size_type=None) : 

        #args check       
        assert isinstance(enable, bool)  

        if enable :  
            assert isinstance(size_val, int)  or  isinstance(size_val, float)
            assert isinstance(size_type, str)
            assert size_type in ["val", "%"]
            if size_type == "val" : assert ((size_val >= 1) and (100 >= size_val))
            else  :                 assert ((size_val >0.0) and (1.0 >= size_val))

        else : 
            size_val    = 0.0
            size_type   = "%"

        self.enable         = enable
        self.size_val       = size_val
        self.size_type      = size_type
        self._open_trade    = False
        self._last_buy      = 0.0

    def __get_open_trade(self) : 
        return self._open_trade

    def __get_last_buy(self) : 
        return self._last_buy

    def __set_open_trade(self, val) :
        assert isinstance(val, bool) 
        self._open_trade = val

    def __set_last_buy(self, val) : 
        assert (isinstance(val, float) or isinstance(val, int))
        assert ((val >= 0.0) and (100000.0 >= val)) 
        self._last_buy = val

    open_trade  = property(__get_open_trade, __set_open_trade)
    last_buy    = property(__get_last_buy, __set_last_buy)

    def __repr__(self) : 
        return str(self.__dict__).replace(",", ";\n").replace(":", "=")


class TradingParams() : 

    def __init__(   self, version, enable_multi_trade, multi_trade_max, 
                    enable_long, enable_short, 
                    dual_bank, bank_init, 
                    long_size_val=1,   long_size_type="%",
                    short_size_val=1, short_size_type="%"): 


        self.bank        = Bank(dual_bank, bank_init) 
        self.multi_trade = MultiTrade(version, enable_multi_trade, multi_trade_max)
        self.long        = Position(enable_long, long_size_val, long_size_type)
        self.short       = Position(enable_short,short_size_val, short_size_type)
        self.price       = Price()
        self.first       = True

   

    def update_before_trading(self, df, ref_price) : 

        # agrs check
        assert isinstance(df, pd.DataFrame)

        self.first                  = True
        self.long.open_trade        = False        
        self.long.last_buy          = 0.0

        self.short.open_trade       = False        
        self.short.last_buy         = 0.0

        self.price.ref              = ref_price
        
        # for average and close_open you have to buy at close
        if  self.price.ref in ["average", "clos_op"] :      self.price.mkt = "close"
        elif self.price.ref in ["high", "low", ""] :        raise ValueError("invalid ref_price")
        else :                                              self.price.mkt = self.price.ref

        # update bank init as required

        if self.bank.dual : 

            if (self.multi_trade.version == "trading") and self.long.enable and (self.bank.long_init<=0.0): 
                self.bank.long_init = df.loc[0, self.price.mkt ]

            if (self.multi_trade.version == "trading") and self.short.enable and (self.bank.short_init<=0.0): 
                self.bank.short_init = df.loc[0, self.price.mkt ]

            if (self.multi_trade.version == "invest") and self.long.enable : 
                if self.long.size_type == "val" : 
                    self.bank.long_init = self.long.size_val * len(df)
                else : 
                    raise ValueError("Invest + Long + size_type % not compatible")

            if not self.long.enable : 
                self.bank.long_init = 0.0

            if not self.short.enable : 
                self.bank.short_init = 0.0

        else : 

            if (self.multi_trade.version == "trading") and self.bank.init<=0.0: 
                self.bank.init   = df.loc[0, self.price.mkt ]

            if (self.multi_trade.version == "invest") and self.long.enable : 
                if self.long.size_type == "val" : 
                    self.bank.init = self.long.size_val * len(df)
                else : 
                    raise ValueError("Invest + Long + size_type % not compatible")

        if (self.multi_trade.version == "invest") and not self.long.enable : 
                raise ValueError("please enable long for invest")

        if (self.multi_trade.version == "invest") and self.short.enable : 
            raise ValueError("Invest + short not avialable")

    def copy(self) : 
        return TradingParams( self.multi_trade.version, self.multi_trade.enable, self.multi_trade.multi_trade_max, 
                    self.long.enable, self.short.enable, 
                    self.bank.dual, self.bank.init, 
                    self.long.size_val, self.long.size_type,
                    self.short.size_val, self.short.size_type)

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n\n").replace(": ",": \n") # .replace("{", "{\n\t") # .replace(",", ",\n") 


class Consts() : 

    def __init__(self, **d) : 

        [setattr(self, k, v) for k, v in d.items()]

    def __repr__(self) : 

        return str(self.__dict__).replace(",", ",\n")



# if package and not main

if __name__ != '__main__':

    C = Consts( ENABLE_MULTI_PROCESSING=ENABLE_MULTI_PROCESSING, NB_CORES=NB_CORES,
                PATH=PATH,FILE=FILE, 
                FEES=FEES, SPREAD=SPREAD, ROLL_OVER=ROLL_OVER,
                TIME_SELECT=TIME_SELECT, TIME_START=TIME_START, TIME_STOP=TIME_STOP, FORCE_WORKDAYS=FORCE_WORKDAYS,
                RANDOMIZE=RANDOMIZE, RANDOM_NB=RANDOM_NB, RANDOM_PERIOD_MIN=RANDOM_PERIOD_MIN, RANDOM_PERIOD_MAX=RANDOM_PERIOD_MAX, ENABLE_REVERSE=ENABLE_REVERSE,
                GRAPHS=GRAPHS, TEMP_FILES=TEMP_FILES, PRINT_RESULTS=PRINT_RESULTS,
                VERSION=VERSION,ENABLE_MULTI_TRADE=ENABLE_MULTI_TRADE, MULTI_TRADE_MAX=MULTI_TRADE_MAX, ENABLE_LONG=ENABLE_LONG, ENABLE_SHORT=ENABLE_SHORT, 
                DUAL_BANK=DUAL_BANK, BANK_INIT=BANK_INIT, 
                LONG_SIZE_VAL=LONG_SIZE_VAL, LONG_SIZE_TYPE=LONG_SIZE_TYPE, 
                SHORT_SIZE_VAL=SHORT_SIZE_VAL, SHORT_SIZE_TYPE=SHORT_SIZE_TYPE)

    del ENABLE_MULTI_PROCESSING, NB_CORES,\
        PATH, FILE, FEES, \
        SPREAD, ROLL_OVER, \
        TIME_SELECT, TIME_START, TIME_STOP, FORCE_WORKDAYS,\
        RANDOMIZE, RANDOM_NB, RANDOM_PERIOD_MIN, RANDOM_PERIOD_MAX, ENABLE_REVERSE,\
        GRAPHS, TEMP_FILES, PRINT_RESULTS,\
        VERSION, ENABLE_MULTI_TRADE, MULTI_TRADE_MAX, ENABLE_LONG, ENABLE_SHORT, DUAL_BANK, BANK_INIT,\
        LONG_SIZE_VAL, LONG_SIZE_TYPE, \
        SHORT_SIZE_VAL, SHORT_SIZE_TYPE

    # multiprocessing
    multi_process = MultiProcessing(C.ENABLE_MULTI_PROCESSING, C.NB_CORES)

    # paths
    paths = Path(C.PATH, C.FILE)

    # broker params
    broker = Broker(C.FEES, C.SPREAD, C.ROLL_OVER)

    # time selection
    time_sel = TimeSel(C.TIME_SELECT, C.TIME_START, C.TIME_STOP)

    # random selection
    random_sel = RandomSel(C.RANDOMIZE, C.RANDOM_NB, C.RANDOM_PERIOD_MIN, C.RANDOM_PERIOD_MAX, C.ENABLE_REVERSE)

    # Output
    output = Output(C.GRAPHS, C.TEMP_FILES, C.PRINT_RESULTS, paths.temp_path)

    # tradings params
    trading_params = TradingParams( C.VERSION, C.ENABLE_MULTI_TRADE, C.MULTI_TRADE_MAX, C.ENABLE_LONG, C.ENABLE_SHORT, 
                                    C.DUAL_BANK, C.BANK_INIT,
                                    C.LONG_SIZE_VAL, C.LONG_SIZE_TYPE,
                                    C.SHORT_SIZE_VAL, C.SHORT_SIZE_TYPE)



