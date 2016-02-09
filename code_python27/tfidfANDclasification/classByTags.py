# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 15:21:27 2015

@author: ivan
"""
from __future__ import division
import numpy as np
from lxml import etree
import os
import argparse
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold

#=======================FUNCTION DEFINITION===================================

#Loads the list of different tags from a file
def loadVocabulary(tagsListFile):
    vocab=[]
    return vocab

#returns a vector of the tags of a post    
def tagsToVector(tagsPost,fullTagsList,n):
    tagVector=np.zeros(n,dtype='int')
    for tp in tagsPost:
        if tp in fullTagsList:
            tagVector[fullTagsList.index(tp)]=1
    return tagVector

def getVocabulary(postSetTags):
    allTags=[]
    for postTags in postSetTags:
        allTags+=postTags
    return list(set(allTags))

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
    
def arArToSt(aA):
    st=[]
    for a in aA:
        st.append(a[0])
    return st

def readXMLCorpusFrom(thisDirectory):
    corpusFiles=exploreDir(thisDirectory)
    corpus=[]
    targets=[]
    #indx=0
    for doc in corpusFiles:
        #print doc
        [dat,aut,tag,cat,txt,tit]=parseBlogFile(thisDirectory+doc)
        corpus.append(tag)
        targets.append(cat)
    return [corpus,targets]

#transforms a list of post in a directory into a matrix
#listOfPosts = a list of lists of tags one list per post
#tagsList = the complete list of tags   
def vectorizePostSetToTags(listOfPosts,tagsList):
    #explore the directory and get tags list per post
    matrxList=[]
    n=len(tagsList)
    for post in listOfPosts:
        matrxList.append(tagsToVector(post,tagsList,n))
    matrixTG=np.matrix(matrxList)
    return matrixTG
    


#============================================================================
    
#======================ACTUAL RUNNING PROGRAM================================
#-----------[mod1]-Receive and parse program arguments------------------------
parser = argparse.ArgumentParser()
parser.add_argument('corpusloc', help='corpus location')
parser.add_argument('-f', dest="nkf", type=int, default=10, help='Number of Folds, default=15')
args = parser.parse_args()
if args.corpusloc[-1]!='/':
    args.corpusloc+='/'
#-----------[mod1]-End--------------------------------------------------------

#-----------[mod2]-Loading corpus, instances and target labels----------------
[inst,labels]=readXMLCorpusFrom(args.corpusloc)
classs=arArToSt(labels)
#-----------[mod2]-End--------------------------------------------------------

#-----------[mod3]-Features space calculation and vectorizing instances-------
features=getVocabulary(inst)
matrix=vectorizePostSetToTags(inst,features)
#-----------[mod3]-End--------------------------------------------------------

#-----------[mod4]-KFold cross validation experiment on 4 classifiers---------
f=1
print "<Experiment for data located in "+args.corpusloc+">"
print "Size of matrix:"+str(matrix.shape)
kf = KFold(len(inst), n_folds=args.nkf)
for train, test in kf:
    #Split set into fold train and test sets
    x_train=np.array(inst)[train]
    x_test=np.array(inst)[test]
    y_train=np.array(classs)[train]
    y_test=np.array(classs)[test]
    
    print "<Results for Fold["+str(f)+"]>"
    features=getVocabulary(x_train)
    X_train=vectorizePostSetToTags(x_train,features)
    print "Fold train Matrix["+str(f)+"]:"+str(X_train.shape)
    X_test=vectorizePostSetToTags(x_test,features)
    print "Fold test Matrix["+str(f)+"]:"+str(X_test.shape)
    
    #Create and train classifiers
    clf_svm = svm.SVC(kernel='linear')
    clf_svm.fit(X_train, y_train)
    
    clf_mNB=MultinomialNB()
    clf_mNB.fit(X_train, y_train)
    
    clf_knn = KNeighborsClassifier()
    clf_knn.fit(X_train, y_train)
    
    clf_ada=RandomForestClassifier(n_estimators=25)
    clf_ada.fit(X_train, y_train)
    #Evaluate the models and output accuracies
    print "Linear SVM Classifier Accuracy:"+str(clf_svm.score(X_test, y_test))
    print "Multinomial Naive Bayes Accuracy:"+str(clf_mNB.score(X_test, y_test))
    print "5 Nearest Neighbors Accuracy:"+str(clf_knn.score(X_test, y_test))
    print "Random Forest (25 learners) Accuracy:"+str(clf_ada.score(X_test, y_test))
    #Obtain the predicted labels for the test subsets
    predicted_svm = clf_svm.predict(X_test)
    predicted_mNB = clf_mNB.predict(X_test)
    predicted_knn = clf_knn.predict(X_test)    
    predicted_ada = clf_ada.predict(X_test)
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
#-----------[mod4]-End--------------------------------------------------------