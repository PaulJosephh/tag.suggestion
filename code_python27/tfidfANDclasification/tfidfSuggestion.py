# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:40:12 2015

@author: ivan
"""
from __future__ import division
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import argparse
from lxml import etree
import cPickle
import os
import time
import numpy as np

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
                if tg.lower() in tprop:
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
                if tg.lower() in tprop:
                    count+=1
        if len(tgs[x])> 0 :
            recArr.append(count/len(tgs[x]))
    return np.mean(recArr), recArr
    
def f1measure(a,b):
    return 2*(a*b)/(a+b)
    
def mergeList(l1,l2):
    n=len(l1)
    l3=[]
    for x in range(n):
        l3.append(list(set(l1[x]+l2[x])))
    return l3

parser = argparse.ArgumentParser()
parser.add_argument('corpusloc', help='corpus location')
parser.add_argument('resultfile', help='file storing results')
parser.add_argument('--n', dest="nTOpropose", type=int, default=15, help='how many tags will be proposed, default=15')
parser.add_argument('--ngram', dest="ngram", type=int, default=2, help='max size of the n-grams considered, default=2')
args = parser.parse_args()
if args.corpusloc[-1]!='/':
    args.corpusloc+='/'

topn=0-args.nTOpropose
stpwrds=loadStopwords("stopwords.french.list")
#print len(stpwrds)
start = time.time()
vectorizer = CountVectorizer(ngram_range=(1,args.ngram),lowercase=True,stop_words=stpwrds)
[txtCorpus,tagsw]=readXMLCorpusFrom(args.corpusloc)
#print tagsw[11]
#print len(txtCorpus)
countMatrix = vectorizer.fit_transform(txtCorpus)
#--------------------------------------

topsTF=[]
for aPost in countMatrix:
    topOfX=[]
    top5=aPost.toarray().argsort()[0]
    for att in top5[topn:]:
        topOfX.append(vectorizer.get_feature_names()[att])
    topsTF.append(topOfX)
#--------------------------------------

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(countMatrix)

#--------------------------------------
topsTFIDF=[]
for aPost in tfidf:
    topOfX=[]
    top5=aPost.toarray().argsort()[0]
    for att in top5[topn:]:
        topOfX.append(vectorizer.get_feature_names()[att])
    topsTFIDF.append(topOfX)

f=open('../../results/tfidfsuggestion/'+args.resultfile+"_"+str(args.nTOpropose)+".res", 'wb')

cPickle.dump(topsTF, f)
cPickle.dump(topsTFIDF, f)
#cPickle.dump(tagsw, f)
f.close()

end = time.time()
print "processing time: "+str(end - start)
start = time.time()
#print topsTF[11]
#print topsTFIDF[11]
#print tagsw[11][3].lower() in topsTFIDF[11][0]
print "-------------------------------"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF,tagsw)
[avrec,recs]=evalAvRecall(topsTF,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
print "Evaluation of TFIDF approach"
[avprecIDF,precsIDF]=evalAvPrecision(topsTFIDF,tagsw)
[avrecIDF,recsIDF]=evalAvRecall(topsTFIDF,tagsw)
print "Precision "+str(avprecIDF)
print "Recall "+str(avrecIDF)
print "F1-measure "+str(f1measure(avprecIDF,avrecIDF))
print "-------------------------------"
print "Evaluation of Together approach"
tops2=mergeList(topsTF,topsTFIDF)
[avprec2,precs2]=evalAvPrecision(tops2,tagsw)
[avrec2,recs2]=evalAvRecall(tops2,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)
