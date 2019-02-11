#!/usr/bin/env python3
# coding: utf-8



import numpy as np
import pandas as pd
from collections import Iterable
from itertools import product
import os
from src.misc import pk_load, pk_save



# Results class
# -----------------------------------------------------------

class Results() : 
    
    def __init__(self, axis_struct, data_label, start_stop, filename="None", strategy_name="None"): 

        assert isinstance(axis_struct,  Iterable)
        for i in axis_struct : 
            assert isinstance(i, str)
            
        assert isinstance(data_label, Iterable)
        for i in data_label : 
            assert isinstance(i, str)

        assert isinstance(start_stop, Iterable)

        self.m = list()

        self.axis_struct = axis_struct + data_label
        self.data_label = data_label
        self.droped_axis = []
        self.start_stop = start_stop
        self.strategy_name = strategy_name
        self.filename = filename


    def __repr__(self) : 
        return f"{self.axis_struct}\n{self.start_stop}\n"





    def sep_trd_mkt_results(self) : 

        new_shape = self.m.shape[:-1]
        self.mkt_results = np.zeros(new_shape)
        self.trd_results = np.zeros(new_shape)

        for i, j, k in product(*[list(range(self.m.shape[i])) for i in [i for i,j in enumerate(new_shape)]]):
            self.mkt_results[i,j,k] = self.m[i,j,k,1]
            self.trd_results[i,j,k] = self.m[i,j,k,0]



    def load(self, paths) : 

        # build good results file list
        filelist = os.listdir(paths.temp_path_results)
        filelist = [i for i in filelist if ".pk" in i]
        filelist = [i.replace(".pk", "") for i in filelist ]

        # create  df results
        self.m = [pk_load(i,  paths.temp_path_results) for i in filelist]
        self.m = pd.DataFrame(self.m, columns=self.axis_struct )

        # del temp results files
        _ = [os.remove(paths.temp_path_results + filename + ".pk") for filename in filelist]

        # reduce dim if possible
        droped_axis = list()

        for c in self.m.columns : 
            if len(self.m[c].unique()) == 1 :   droped_axis.append(c)
            elif len(self.m[c].unique()) < 1 :  raise ValueError("error")
            else :                              pass

        droped_values = [self.m[c].iloc[0] for c in droped_axis]
        self.m.drop(droped_axis, axis=1, inplace=True)
        self.droped_axis = [(i,j) for i,j in zip(droped_axis, droped_values)]   

        # resort 
        sort_cols = [i for i in self.m.columns if i not in ("trd", "mkt", "time")]
        self.m.sort_values(sort_cols, inplace=True)
        self.m.index = list(range(len(self.m)))

        # pk_save
        pk_save(self, "results", paths.temp_path)


    def force_reindex(self) : 

        assert isinstance(self.m, pd.DataFrame)
        cols = [i for i in self.m.columns if i not in self.data_label]
        self.m.set_index(cols, inplace=True, drop=True)







