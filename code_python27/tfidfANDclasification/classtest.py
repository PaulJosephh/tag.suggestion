# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 18:40:12 2015

@author: ivan
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import argparse
from lxml import etree
import cPickle
import os

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

parser = argparse.ArgumentParser()
parser.add_argument('corpusloc', help='corpus location')
#parser.add_argument('resultfile', help='file storing results')
args = parser.parse_args()
if args.corpusloc[-1]!='/':
    args.corpusloc+='/'

stpwrds=loadStopwords("stopwords.french.list")
#print len(stpwrds)
vectorizer = CountVectorizer(ngram_range=(1,2),lowercase=True,stop_words=stpwrds)
[txtCorpus,tagsw]=readXMLCorpusFrom(args.corpusloc)
#print tagsw[11]
#print len(txtCorpus)
countMatrix = vectorizer.fit_transform(txtCorpus)
#--------------------------------------
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(countMatrix)
#--------------------------------------
