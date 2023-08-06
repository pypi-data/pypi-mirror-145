#!/usr/bin/env python
"""test"""

# pylint: disable= invalid-name

import sys
import multiprocessing

l= [0] * 10;

def f(tp):
    """test"""
    #print(f"startn f({tp!r})\n")
    x, n= tp
    try:
        z= 1/x
        print(f"end f({tp!r})\n")
        return z
    except ZeroDivisionError as e:
        raise ValueError("call %d: %s" % (n, str(e))) from None

def test():
    """test"""
    args_list=[(0,0), (3,1), (6,2), (3,3), (1,4)]
    with multiprocessing.Pool() as pool:
        print("start")
        res= pool.map_async(f, args_list)
        print("end")
        res.get()

try:
    test()
except ValueError as e:
    #print(f"#### L: {l!r}")
    sys.exit(str(e))
#print(f"#### L: {l!r}")
print("program end")
