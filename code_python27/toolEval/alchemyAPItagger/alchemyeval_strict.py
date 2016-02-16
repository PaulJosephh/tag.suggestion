# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:40:12 2015

@author: ivan
"""
from __future__ import division
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
import argparse
from lxml import etree
import cPickle
import os
import time
import numpy as np
from alchemyapi import AlchemyAPI
import json

def parseBlogFile(myfile):
    f=open(myfile)
    document = etree.fromstring(f.read())
    
    date=document.xpath("date/text()")
#    print date[0]
    
    title=document.xpath("title/text()")
#    print title[0]    
    
    author=document.xpath("author/text()")
#   print author[0]
    
    tags=document.xpath("tags_set/tag/text()")
#    for tag in tags:
#        print tag.text
    
    cats=document.xpath("categories_set/category/text()")
#    for cat in cats:
#       print cat.text
        
    text=document.xpath("text/text()")[0]
#    print text
    
    return (date, author, tags, cats, text, title)

def exploreDir(targetDir):
    f=[]
    for (dirpath,dirnames,filenames) in os.walk(targetDir):
        f.extend(filenames)
        break
    return f

def readXMLCorpusFrom(thisDirectory):
    corpusFiles=exploreDir(thisDirectory)
    corpus=[]
    tagw=[]
    #indx=0
    for doc in corpusFiles:
        #print doc
        [dat,aut,tag,cat,txt,tit]=parseBlogFile(thisDirectory+doc)
        corpus.append(txt)
        #print type(tag)
        tagw.append(tag)
        #if indx==11:
        #    print tag
            #print tit
        #indx+=1
    return [corpus,tagw]

def loadStopwords(listfile):
    lf=open(listfile)
    stopwordlst=[]
    for word in lf.readlines():
        word=word.replace('\n',"")
        stopwordlst.append(unicode(word,'utf8'))
        #print word
    return stopwordlst
    
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
                #if x==11:
                #    print tg.lower()+" "+tprop
                if tg.lower() == tprop:
                    #if x==11:
                    #    print tg.lower()+" "+tprop
                    count+=1
        #if x==11:
        #    print strcount
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
    if (a+b)>0:
        return 2*(a*b)/(a+b)
    else:
        return 0
    
def mergeList(l1,l2):
    n=len(l1)
    l3=[]
    for x in range(n):
        l3.append(list(set(l1[x]+l2[x])))
    return l3

parser = argparse.ArgumentParser()
parser.add_argument('corpusloc', help='corpus location')
parser.add_argument('resultfile', help='file storing results')
parser.add_argument('--n', dest="nTOpropose", type=int, default=10, help='how many tags will be proposed, default=10')
parser.add_argument('--ngram', dest="ngram", type=int, default=2, help='max size of the n-grams considered, default=2')
args = parser.parse_args()
if args.corpusloc[-1]!='/':
    args.corpusloc+='/'

topn=0-args.nTOpropose
#stpwrds=loadStopwords("stopwords.french.list")
#print len(stpwrds)
start = time.time()
#vectorizer = CountVectorizer(ngram_range=(1,args.ngram),lowercase=True,stop_words=stpwrds)
[txtCorpus,tagsw]=readXMLCorpusFrom(args.corpusloc)
#print tagsw[11]
#print len(txtCorpus)
tgsugtop=[]
alchemyapi = AlchemyAPI()
for docX in txtCorpus:
    #print docX
    tagsug=[]
    response = alchemyapi.combined('text', docX)
    if response['status'] == 'OK':
        for keyword in response['keywords']:
            tagsug.append([keyword['text'],keyword['relevance']])
        for entity in response['entities']:
            tagsug.append([entity['text'],entity['relevance']])
        for tgsg in sorted(tagsug, key=lambda x: x[1])[:10]:
            tgsugtop.append(tgsg[0])
            print tgsg[0]

#--------------------------------------


#f=open('../../results/tfidfsuggestion/'+args.resultfile+"_"+str(args.nTOpropose)+".res", 'wb')
f=open("../../../results/tooleval/alchemyAPItagger/"+args.resultfile+"_"+str(args.nTOpropose)+".res", 'wb')

cPickle.dump(tgsugtop, f)
#cPickle.dump(tagsw, f)
f.close()

end = time.time()
print "processing time: "+str(end - start)
start = time.time()
print "Evaluation AlchemyAPI tagger:"
[avprec2,precs2]=evalAvPrecision(tgsugtop,tagsw)
[avrec2,recs2]=evalAvRecall(tgsugtop,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)