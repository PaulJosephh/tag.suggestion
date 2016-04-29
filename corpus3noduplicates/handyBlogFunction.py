# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 21:30:36 2015

@author: ivan
"""

import datetime
import os
from lxml import etree
from collections import Counter

def parseBlogFile(myfile):
    f=open(myfile)
    document = etree.fromstring(f.read())
    
    date=document.xpath("date/text()")
    
    author=document.xpath("author/text()")

    title=document.xpath("title/text()")    
    
    tags=document.xpath("tags_set/tag/text()")
    
    cats=document.xpath("categories_set/category/text()")
        
    text=document.xpath("text/text()")[0]
    
    return (date, author, tags, cats, text, title)

def exploreDir(targetDir):
    f=[]
    for (dirpath,dirnames,filenames) in os.walk(targetDir):
        f.extend(filenames)
        break
    return f
    
def stdDate_blog_josdblog(indate):
    tmpDateArray=indate.split(" ")
    mois=josdblogMonth(tmpDateArray[1])
    ret_date=datetime.date(int(tmpDateArray[2]),mois,int(tmpDateArray[0]))
    return ret_date
    
def josdblogMonth(argument):
    switcher = {"janvier": 1,
        "fvrier": 2,
        "mars": 3,
        "avril": 4,
        "mai": 5,
        "juin": 6,
        "juillet": 7,
        "aot": 8,
        "septembre": 9,
        "octobre": 10,
        "novembre": 11,
        "dcembre": 12}
    return switcher.get(argument, 01)