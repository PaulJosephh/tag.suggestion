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
parser.add_argument('--n', dest="nTOpropose", type=int, default=25, help='how many tags will be proposed, default=15')
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


topsTF25=[]
topsTF20=[]
topsTF15=[]
topsTF10=[]
topsTF5=[]

for aPost in countMatrix:
    topOf25=[]
    topOf20=[]
    topOf15=[]
    topOf10=[]
    topOf5=[]
    top5=aPost.toarray().argsort()[0]
    for att in top5[-25:]:
        topOf25.append(vectorizer.get_feature_names()[att])
    for att in top5[-20:]:
        topOf20.append(vectorizer.get_feature_names()[att])
    for att in top5[-15:]:
        topOf15.append(vectorizer.get_feature_names()[att])
    for att in top5[-10:]:
        topOf10.append(vectorizer.get_feature_names()[att])
    for att in top5[-5:]:
        topOf5.append(vectorizer.get_feature_names()[att])
    topsTF25.append(topOf25)
    topsTF20.append(topOf20)
    topsTF15.append(topOf15)
    topsTF10.append(topOf10)
    topsTF5.append(topOf5)
#--------------------------------------

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(countMatrix)

#--------------------------------------
topsTFIDF25=[]
topsTFIDF20=[]
topsTFIDF15=[]
topsTFIDF10=[]
topsTFIDF5=[]

for aPost in countMatrix:
    topOf25=[]
    topOf20=[]
    topOf15=[]
    topOf10=[]
    topOf5=[]
    top5=aPost.toarray().argsort()[0]
    for att in top5[-25:]:
        topOf25.append(vectorizer.get_feature_names()[att])
    for att in top5[-20:]:
        topOf20.append(vectorizer.get_feature_names()[att])
    for att in top5[-15:]:
        topOf15.append(vectorizer.get_feature_names()[att])
    for att in top5[-10:]:
        topOf10.append(vectorizer.get_feature_names()[att])
    for att in top5[-5:]:
        topOf5.append(vectorizer.get_feature_names()[att])
    topsTFIDF25.append(topOf25)
    topsTFIDF20.append(topOf20)
    topsTFIDF15.append(topOf15)
    topsTFIDF10.append(topOf10)
    topsTFIDF5.append(topOf5)

f=open('../experiments/experiments1/'+args.resultfile+"_"+str(args.nTOpropose)+".res", 'wb')

cPickle.dump(topsTF25, f)
cPickle.dump(topsTFIDF25, f)

cPickle.dump(topsTF20, f)
cPickle.dump(topsTFIDF20, f)

cPickle.dump(topsTF15, f)
cPickle.dump(topsTFIDF15, f)

cPickle.dump(topsTF10, f)
cPickle.dump(topsTFIDF10, f)

cPickle.dump(topsTF5, f)
cPickle.dump(topsTFIDF5, f)
#cPickle.dump(tagsw, f)
f.close()

end = time.time()
print "processing time: "+str(end - start)
start = time.time()
#print topsTF[11]
#print topsTFIDF[11]
#print tagsw[11][3].lower() in topsTFIDF[11][0]
print "-------------------------------25"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF25,tagsw)
[avrec,recs]=evalAvRecall(topsTF25,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
print "Evaluation of TFIDF approach"
[avprecIDF,precsIDF]=evalAvPrecision(topsTFIDF25,tagsw)
[avrecIDF,recsIDF]=evalAvRecall(topsTFIDF25,tagsw)
print "Precision "+str(avprecIDF)
print "Recall "+str(avrecIDF)
print "F1-measure "+str(f1measure(avprecIDF,avrecIDF))
print "-------------------------------"
print "Evaluation of Together approach"
tops2=mergeList(topsTF25,topsTFIDF25)
[avprec2,precs2]=evalAvPrecision(tops2,tagsw)
[avrec2,recs2]=evalAvRecall(tops2,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)

print "-------------------------------20"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF20,tagsw)
[avrec,recs]=evalAvRecall(topsTF20,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
print "Evaluation of TFIDF approach"
[avprecIDF,precsIDF]=evalAvPrecision(topsTFIDF20,tagsw)
[avrecIDF,recsIDF]=evalAvRecall(topsTFIDF20,tagsw)
print "Precision "+str(avprecIDF)
print "Recall "+str(avrecIDF)
print "F1-measure "+str(f1measure(avprecIDF,avrecIDF))
print "-------------------------------"
print "Evaluation of Together approach"
tops2=mergeList(topsTF20,topsTFIDF20)
[avprec2,precs2]=evalAvPrecision(tops2,tagsw)
[avrec2,recs2]=evalAvRecall(tops2,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)

print "-------------------------------15"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF15,tagsw)
[avrec,recs]=evalAvRecall(topsTF15,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
print "Evaluation of TFIDF approach"
[avprecIDF,precsIDF]=evalAvPrecision(topsTFIDF15,tagsw)
[avrecIDF,recsIDF]=evalAvRecall(topsTFIDF15,tagsw)
print "Precision "+str(avprecIDF)
print "Recall "+str(avrecIDF)
print "F1-measure "+str(f1measure(avprecIDF,avrecIDF))
print "-------------------------------"
print "Evaluation of Together approach"
tops2=mergeList(topsTF15,topsTFIDF15)
[avprec2,precs2]=evalAvPrecision(tops2,tagsw)
[avrec2,recs2]=evalAvRecall(tops2,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)

print "-------------------------------10"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF10,tagsw)
[avrec,recs]=evalAvRecall(topsTF10,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
print "Evaluation of TFIDF approach"
[avprecIDF,precsIDF]=evalAvPrecision(topsTFIDF10,tagsw)
[avrecIDF,recsIDF]=evalAvRecall(topsTFIDF10,tagsw)
print "Precision "+str(avprecIDF)
print "Recall "+str(avrecIDF)
print "F1-measure "+str(f1measure(avprecIDF,avrecIDF))
print "-------------------------------"
print "Evaluation of Together approach"
tops2=mergeList(topsTF10,topsTFIDF10)
[avprec2,precs2]=evalAvPrecision(tops2,tagsw)
[avrec2,recs2]=evalAvRecall(tops2,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)

print "-------------------------------5"
print "Evaluation of TF approach"
[avprec,precs]=evalAvPrecision(topsTF5,tagsw)
[avrec,recs]=evalAvRecall(topsTF5,tagsw)
print "evaluated instances "+str(len(precs))
print "Precision "+str(avprec)
print "Recall "+str(avrec)
print "F1-measure "+str(f1measure(avprec,avrec))
print "-------------------------------"
print "Evaluation of TFIDF approach"
[avprecIDF,precsIDF]=evalAvPrecision(topsTFIDF5,tagsw)
[avrecIDF,recsIDF]=evalAvRecall(topsTFIDF5,tagsw)
print "Precision "+str(avprecIDF)
print "Recall "+str(avrecIDF)
print "F1-measure "+str(f1measure(avprecIDF,avrecIDF))
print "-------------------------------"
print "Evaluation of Together approach"
tops2=mergeList(topsTF5,topsTFIDF5)
[avprec2,precs2]=evalAvPrecision(tops2,tagsw)
[avrec2,recs2]=evalAvRecall(tops2,tagsw)
print "Precision "+str(avprec2)
print "Recall "+str(avrec2)
print "F1-measure "+str(f1measure(avprec2,avrec2))

end = time.time()
print "evaluation time: "+str(end - start)