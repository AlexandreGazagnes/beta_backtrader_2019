#!/usr/bin/env python3
# coding: utf-8



import numpy as np
from collections import Iterable
from itertools import product



# Results class
# -----------------------------------------------------------

class Results() : 
    
    def __init__(self, axis_struct, data_label, start_stop, strategy_name): 

        assert isinstance(axis_struct,  Iterable)
        for i,j in axis_struct : 
            assert isinstance(i, str)
            assert isinstance(j, Iterable)
            
        assert isinstance(data_label, Iterable)
        for i in data_label : 
            assert isinstance(i, str)

        assert isinstance(start_stop, Iterable)

        shape = [len(j) for i,j in axis_struct]
        shape.append(len(data_label))
        self.m = np.zeros(shape)

        assert len(axis_struct) + 1 == (len(shape))
        self.axis_struct = axis_struct
        self.data_label = data_label
        self.start_stop = start_stop


    def __repr__(self) : 
        return f"{self.axis_struct}\n{self.data_label}\n{self.start_stop}\n{self.m.shape}"


    def reduce_dims_if_possible(self) : 
        pass


    def sep_trd_mkt_results(self) : 

        new_shape = self.m.shape[:-1]
        self.mkt_results = np.zeros(new_shape)
        self.trd_results = np.zeros(new_shape)

        for i, j, k in product(*[list(range(self.m.shape[i])) for i in [i for i,j in enumerate(new_shape)]]):
            self.mkt_results[i,j,k] = self.m[i,j,k,1]
            self.trd_results[i,j,k] = self.m[i,j,k,0]

