# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 13:26:35 2015

@author: ivan
"""
import numpy as np

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
            
            
#a=["vam","frank","were"]
#b=["piro","einstein","wolf","mummy"]
#mat=[[2,3,4,5],[1,5,2,7],[7,3,3,9]]
#
#
#print test.listA
#print test.listB
#print test.matrixAA
#print test.getWordbyIndxA(2)+test.getWordbyIndxB(2)
#print test.getMatValueByIndx(1,2)
#print test.getRelation("were","mummy")
#print test.getLineByW("were")
#print test.getcolumnByW("piro")
#
#test2=atsMatrix(a,b)
#print test2.matrixAA
#test2.setValueByWord(5, "vam", "mummy")
#test2.setValueByIndx(9, 1, 2)
#print test2.matrixAA
