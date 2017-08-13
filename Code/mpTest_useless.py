# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 23:00:15 2017

@author: felix
"""

from multiprocessing import Pool
from contextlib import closing

def f(x):
    a,b =x
    return a*b

if __name__ == '__main__':
    with closing(Pool(5)) as p:
        print(p.map(f, [[1,1], [2,2], [3,3]]))
        p.terminate()