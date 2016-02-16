# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 23:02:51 2016

@author: ivan
"""
from __future__ import division
import numpy as np
import time
import argparse
from lxml import etree
import os

def evalAvPrecision(prop,tgs):
    n=len(tgs)
    precArr=[]
    #cycle to go through all instances
    for x in range(n):
        count=0
        #cycle to go through actual tags of instance x
        for tg in tgs[x]:
            #cycle to go through proposed tags for instance x
            for tprop in prop[x]:
                if tg.lower() == tprop:
                    count+=1
        if len(tgs[x])> 0 :
            precArr.append(count/len(prop[x]))
    return np.mean(precArr), precArr

def evalAvRecall(prop,tgs):
    n=len(tgs)
    recArr=[]
    #cycle to go through all instances
    for x in range(n):
        count=0
        #cycle to go through actual tags of instance x
        for tg in tgs[x]:
            #cycle to go through proposed tags for instance x
            for tprop in prop[x]:
                if tg.lower()==tprop:
                    count+=1
        if len(tgs[x])> 0 :
            recArr.append(count/len(tgs[x]))
    return np.mean(recArr), recArr
    
def f1measure(a,b):
    return 2*(a*b)/(a+b)

#parsing de cada XML regresa una lista con cada uno de los campos
#en el caso de tags y categorias (cats) regresa una lista
def parseBlogFile(myfile):
    f=open(myfile)
    document = etree.fromstring(f.read())
    
    date=document.xpath("date/text()")
    
    title=document.xpath("title/text()")
    
    author=document.xpath("author/text()")
    
    tags=document.xpath("tags_set/tag/text()")
    
    cats=document.xpath("categories_set/category/text()")
        
    text=document.xpath("text/text()")[0]
   
    return (date, author, tags, cats, text, title)

#recorre un directorio dado y regresa la lista de archivos en el
def exploreDir(targetDir):
    f=[]
    for (dirpath,dirnames,filenames) in os.walk(targetDir):
        f.extend(filenames)
        break
    return f

#lee todos los archivos de un directorio y los parsea
#regresa varias listas con los distintos campos
#en el caso de de tags y cats los regresa como una lista de listas
#corpus son los textos
def readXMLCorpusFrom(thisDirectory):
    corpusFiles=exploreDir(thisDirectory)
    corpus=[]
    tagw=[]
    catw=[]
    for doc in corpusFiles:
        [dat,aut,tag,cat,txt,tit]=parseBlogFile(thisDirectory+doc)
        corpus.append(txt)
        tagw.append(tag)
        catw.append(cat)
    return [corpus,tagw,catw]


parser = argparse.ArgumentParser()
parser.add_argument('corpusloc', help='corpus location')
args = parser.parse_args()
if args.corpusloc[-1]!='/':
    args.corpusloc+='/'
    
[txtCorpus,tagsw,catsw]=readXMLCorpusFrom(args.corpusloc)

#en esta variable se cargaría una lista de listas 
#cada lista dentro de la lista serían los elementos a evaluar
#cada lista representa un documento en este caso un post
topsTF=[]

start = time.time()    
print "-------------------------------"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF,tagsw)
[avrec,recs]=evalAvRecall(topsTF,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
end = time.time()
print "evaluation time: "+str(end - start)