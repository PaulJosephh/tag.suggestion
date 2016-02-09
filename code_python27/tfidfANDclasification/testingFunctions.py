# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:25:26 2015

@author: ivan
"""
from __future__ import division
import argparse

def halfSplit(n):
    if n % 2 == 1:
        return (n+1)/2
    else:
        return n/2
        
def percSplit(n,sz):
    a=int(n*(sz/100))+1
    b=n-a
    return [a,b]
    
def arArToSt(aA):
    st=[]
    for a in aA:
        st.append(a[0])
    return st

parser = argparse.ArgumentParser()
parser.add_argument('m')
parser.add_argument('s')
args = parser.parse_args()
print halfSplit(int(args.m))
print percSplit(int(args.m),int(args.s))