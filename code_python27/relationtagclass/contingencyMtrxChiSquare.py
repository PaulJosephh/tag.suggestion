# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:54:43 2015

@author: ivan
"""
from __future__ import division
import argparse
import os
import time
import numpy as np
from collections import Counter
from scipy import stats
#import cPickle

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

class atsMatrix:
    "atribute vs atribute matrix"
    listA=[]
    listB=[]
    matrixAA=np.array([])
    
    def setListA(self,a):
        self.listA=a
        
    def setListB(self,b):
        self.listB=b
        
    def getWordbyIndxA(self,indx):
        if (indx>(len(self.listA)-1)) or (indx<0):
            print "The index must be within the size of listA, use getLenA() method to retrieve this value."
        else:
            return self.listA[indx]
            
    def getWordbyIndxB(self,indx):
        if (indx>(len(self.listB)-1)) or (indx<0):
            print "The index must be within the size of listB, use getLenB() method to retrieve this value."
        else:
            return self.listB[indx]
            
    def getMatValueByIndx(self,x,y):
        if (x>(len(self.listB)-1)) or (x<0) or (y>(len(self.listA)-1)) or (y<0):
            print "The index must be within the size of listB, use getLenB() method to retrieve this value."
        else:
            return self.matrixAA[x][y]
            
    def getRelation(self,wx,wy):
        if ((wx in self.listA) and (wy in self.listB)):
            x=self.listA.index(wx)
            y=self.listB.index(wy)
            return self.matrixAA[x][y]
        else:
            print "The terms are not indexes of the matrix"
        
    def getLineByW(self,wx):
        if wx in self.listA:
            x=self.listA.index(wx)
            return self.matrixAA[x]
            
    def getcolumnByW(self,wy):
        if wy in self.listB:
            y=self.listB.index(wy)
            return self.matrixAA[:,y]
    
    def getIndxByWordA(self, xw):
        if xw in self.listA:
            return self.listA.index(xw)
            
    def getIndxByWordB(self, xw):
        if xw in self.listB:
            return self.listB.index(xw)
            
    def setValueByWord(self, val, wx, wy):
         if (wx in self.listA) and (wy in self.listB):
             x=self.listA.index(wx)
             y=self.listB.index(wy)
             self.matrixAA[x][y]=val
             
    def setValueByIndx(self, val, x, y):
        self.matrixAA[x][y]=val
        
    def __init__(self, alist, blist,relations=[]):
        relSize=np.shape(relations)
        if relSize[0]>0:
            if (len(alist)==relSize[0]) and (len(blist)==relSize[1]):
                self.listA=alist
                self.listB=blist
                self.matrixAA=relations
            else:
                 print "Uncompatible object sizes. The matrix must be of size n x m, where n is the length of first list, and m the length of second list."   
        else:
            x=len(alist)
            y=len(blist)
            self.listA=alist
            self.listB=blist
            self.matrixAA=np.zeros(shape=(x,y))
            
def exploreDir(targetDir):
    f=[]
    for (dirpath,dirnames,filenames) in os.walk(targetDir):
        f.extend(filenames)
        break
    return f
    
parser = argparse.ArgumentParser()
parser.add_argument('corpusloc', help='corpus location')
parser.add_argument('datanam', help='dataset name')
args = parser.parse_args()
if args.corpusloc[-1]!='/':
    args.corpusloc+='/'
    
categories=exploreDir(args.corpusloc+"categories/")

fcats=open(args.corpusloc+args.datanam+"_cat",'r')
cats=[]
for xcat in fcats:
    cats.append(xcat.replace('\n',""))

ftags=open(args.corpusloc+args.datanam+"_tag",'r')
tagss=[]
for xtag in ftags:
    tagss.append(xtag.replace('\n',""))

start=time.time()

test=atsMatrix(tagss,cats)
#print test.matrixAA.shape

#cat=Counter(categories)

for cat in categories:
    col=test.getIndxByWordB(cat)
    filcat=open(args.corpusloc+"categories/"+cat, 'r')
    ctemp=[]
    for ct in filcat.readlines():
        ctemp.append(ct.replace('\n',""))
    cctemp=Counter(ctemp)
    for atag in cctemp:
        linez=test.getIndxByWordA(atag)
        test.setValueByIndx(cctemp[atag],linez,col)
        #print atag+"--"+str(cctemp[atag])
#print test.matrixAA.nonzero()
#print test.getRelation("update","RFXcom")
#f=open(args.corpusloc+args.datanam+"_contigency.mtx", 'wb')
#cPickle.dump(test, f)
end=time.time()
print end-start
print test.matrixAA.shape
#print stats.chi2_contingency(test.matrixAA,lambda_="log-likelihood")
print stats.power_divergence(test.matrixAA,lambda_="log-likelihood")
#print "Lambda: "+str(lamdaGK(test.matrixAA))
#print "Lambda: "+str(lamdaGKr(test.matrixAA))