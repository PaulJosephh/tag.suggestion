# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 17:36:34 2015

@author: ivan
"""
from __future__ import division
from lxml import etree
import os
import argparse
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
#from collections import Counter
from sklearn.cross_validation import StratifiedKFold
#Split data into training and test subsets
#receives the percentage of instances training subset
def percSplit(n,sz):
    a=int(n*(sz/100))+1
    b=n-a
    return [a,b]

def halfSplit(n):
    if n % 2 == 1:
        return (n+1)/2
    else:
        return n/2

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
    targets=[]
    #indx=0
    for doc in corpusFiles:
        #print doc
        [dat,aut,tag,cat,txt,tit]=parseBlogFile(thisDirectory+doc)
        corpus.append(txt)
        targets.append(cat)
    return [corpus,targets]

def arArToSt(aA):
    st=[]
    for a in aA:
        st.append(a[0])
    return st

def cutSubsetsFromIndx(bigXset,bigYset,indexs):
    subsetX=[]
    subsetY=[]
    for i in indexs:
        subsetX.append(bigXset[i])
        subsetY.append(bigYset[i])
    return subsetX,subsetY
    
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
parser.add_argument('-p',dest="trainsize", type=int, default=50, help='percentage of instances used for training')
#parser.add_argument('resultfile', help='file storing results')
args = parser.parse_args()
#print len(exploreDir(args.corpusloc))
[inst,labels]=readXMLCorpusFrom(args.corpusloc)

classs=arArToSt(labels)
print len(classs)
print len(inst)

stpwrds=loadStopwords("stopwords.french.list")
vectorizer = CountVectorizer(ngram_range=(1,2),lowercase=True,stop_words=stpwrds)

print "<Experiment for data located in "+args.corpusloc+">"
#print "Size of matrix:"+str(inst.shape)

kf = KFold(len(inst), n_folds=10)
f=1
for train, test in kf:
    print "<Results for Fold["+str(f)+"]>"
#    print "Fold Matrix["+str(f)+"]:"+str(vtrset.shape)    
    
    X_train=np.array(inst)[train]
    X_test=np.array(inst)[test]
    y_train=np.array(classs)[train]
    y_test=np.array(classs)[test]
       
    countMatrix_train = vectorizer.fit_transform(X_train)
    countMatrix_test = vectorizer.transform(X_test)
    
    countMatrix_train2 = vectorizer.fit_transform(X_test)
    countMatrix_test2 = vectorizer.transform(X_train)
    
    print "Fold train Matrix["+str(f)+"]:"+str(countMatrix_train.shape)
    print "Fold test Matrix["+str(f)+"]:"+str(countMatrix_test.shape)
    
    #print countMatrix_train.shape
    #print countMatrix_test.shape
    #--------------------------------------
    transformer = TfidfTransformer()
    tfidf_train = transformer.fit_transform(countMatrix_train)
    tfidf_test = transformer.transform(countMatrix_test)
    
    tfidf_train2 = transformer.fit_transform(countMatrix_train2)
    tfidf_test2 = transformer.transform(countMatrix_test2)
    
    print tfidf_train.shape
    print tfidf_test.shape
    
    clf_svm = svm.SVC(kernel='linear')
    clf_svm.fit(tfidf_train, y_train)
    
    clf_mNB=MultinomialNB()
    clf_mNB.fit(tfidf_train, y_train)
    
    clf_knn = KNeighborsClassifier()
    clf_knn.fit(tfidf_train, y_train)
    
    clf_ada=RandomForestClassifier(n_estimators=25)
    clf_ada.fit(tfidf_train, y_train)
    
    #Evaluate the models and output accuracies
    print "Linear SVM Classifier Accuracy:"+str(clf_svm.score(tfidf_test, y_test))
    print "Multinomial Naive Bayes Accuracy:"+str(clf_mNB.score(tfidf_test, y_test))
    print "5 Nearest Neighbors Accuracy:"+str(clf_knn.score(tfidf_test, y_test))
    print "Random Forest (25 learners) Accuracy:"+str(clf_ada.score(tfidf_test, y_test))
    #Obtain the predicted labels for the test subsets
    
    #print clf_svm.score(tfidf_test, y_test)
    #print clf_mNB.score(tfidf_test, y_test)
    #print clf_knn.score(tfidf_test, y_test)
    #print clf_ada.score(tfidf_test, y_test)
    #Obtain the predicted labels for the test subsets
    predicted_svm = clf_svm.predict(tfidf_test) 
    predicted_mNB = clf_mNB.predict(tfidf_test) 
    predicted_knn = clf_knn.predict(tfidf_test) 
    predicted_ada = clf_ada.predict(tfidf_test)
    
     #output metrics on the evaluation
    print "<Linear SVM Classifier Metrics>"
    print(metrics.classification_report(y_test, predicted_svm))
    print "<Multinomial Naive Bayes Classifier Metrics>"
    print(metrics.classification_report(y_test, predicted_mNB))
    print "<5 Nearest Neighbors Classifier Metrics>"
    print(metrics.classification_report(y_test, predicted_knn))
    print "<Random Forest (25 learners) Classifier Metrics>"
    print(metrics.classification_report(y_test, predicted_ada))
    
    f+=1