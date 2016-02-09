# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:14:55 2015

@author: ivan
"""
from __future__ import division
import numpy as np

def lamdaGK(mtrx):
    #Goodman-Kruskal Lambda
    #totalsCols=mtrx.sum(0)
    totalsLins=mtrx.sum(1)
    N=totalsLins.sum()
    
    Mdv=totalsLins.max()
    ncols=mtrx.shape[0]
    
    Fiv=0
    for i in range(ncols):
        Fiv+=mtrx[i].max()
    GKlambda=(Fiv-Mdv)/(N-Mdv)
    return GKlambda
    
def lamdaGKr(mtrx):
    #Goodman-Kruskal Lambda
    totalsCols=mtrx.sum(0)
    #totalsLins=mtrx.sum(1)
    N=totalsCols.sum()
    
    Mdv=totalsCols.max()
    ncols=mtrx.shape[1]
    
    Fiv=0
    for i in range(ncols):
        Fiv+=mtrx[:,i].max()
    GKlambda=(Fiv-Mdv)/(N-Mdv)
    return GKlambda
    
musfood=np.array([[8,52,20],[55,18,39],[47,8,84]])
print musfood
print lamdaGK(musfood)
print lamdaGKr(musfood)