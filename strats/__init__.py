#!/usr/bin/env python3
# coding: utf-8


import os 
__all__ = [i.replace(".py", "") for i in os.listdir(os.getcwd()+"/strats/") if "__" not in i]


