# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:42:20 2015

@author: ivan
"""

import handyBlogFunction as toolkit
import mysql.connector
import re

#function declaration area

def importBlogToDB(blogdir,cnx,blogName,url):
    dbHand = cnx.cursor()
#insert the new blog into blog table and retrieve id
    query="INSERT INTO blog (blogName,url) VALUE ('"+blogName+"','"+url+"');"   
    dbHand.execute(query)
    idx = dbHand.lastrowid
    cnx.commit()
#explore the blog's directory
    entries=toolkit.exploreDir(blogdir)
#for each file (post) in directory
    for x in entries:
        print x
    #----parse xml file and retrieve data
        [date, author, tags, cats, text, title]=toolkit.parseBlogFile(blogdir+x)
#----insert a record in blogEntry(title,blog,file,author,date)
        if len(date)>0:
            query="INSERT INTO post (title,blog,file,date,author) VALUES ('"+re.escape(title[0])+"',"+str(idx)+",'"+x+"','"+date[0]+"','"+re.escape(author[0])+"');"
            dbHand.execute(query)
            idEntry=dbHand.lastrowid
            cnx.commit()
#----for each category
            if len(cats)>0:
#--------search for each category in file if already exists
                for cat in cats:
                    dbHand.execute("SELECT idcategory FROM category where categoryName='"+re.escape(cat)+"' and blog="+str(idx)+";")
                    res=dbHand.fetchall()
#--------if it doesnt insert a record in category(post,cat)
                    if dbHand.rowcount == (0):
                        query="INSERT INTO category (categoryName,blog) VALUES ('"+re.escape(cat)+"',"+str(idx)+");"
                        dbHand.execute(query)
                        cnx.commit()
#--------obtain the id of the category from category table
                        idCat=dbHand.lastrowid
                    else :
                        idCat=res[0][0]
#--------insert in a record in catEntry(post,cat)
                    query="INSERT INTO category_link (cat,entry) VALUES ("+str(idCat)+","+str(idEntry)+");"
                    dbHand.execute(query)
                    cnx.commit()
#----for each tag
            if len(tags)>0:
#--------search for each tag in file if already exists
                for tag in tags:
                    dbHand.execute("SELECT idtag FROM tag where tag='"+re.escape(tag)+"' and blog="+str(idx)+";")
                    res=dbHand.fetchall()
#--------if it doesnt insert a record in tag(post,tag)
                    if dbHand.rowcount == (0):
                        query="INSERT INTO tag (tag,blog) VALUES ('"+re.escape(tag)+"',"+str(idx)+");"
                        dbHand.execute(query)
                        cnx.commit()
#--------obtain the id of the tag from tag table
                        idTag=dbHand.lastrowid
                    else :
                        idTag=res[0][0]
#--------insert in a record in tagEntry(post,tag)
                    query="INSERT INTO tag_link (tag,entry) VALUES ("+str(idTag)+","+str(idEntry)+");"
                    dbHand.execute(query)
                    cnx.commit()


#obtain parameters
#create objects for handling connection
#connect to blogs database
cnx = mysql.connector.connect(user='ivan',password='mysql2311',host='127.0.0.1',database='fr_blog_corpus_DB')
cursor1=cnx.cursor()
importBlogToDB("corpus2_dates/xbcommebon/",cnx,"bcommebon","http://bcommebon.canalblog.com/")
importBlogToDB("corpus2_dates/xbeaualalouche/",cnx,"beaualalouche","http://www.beaualalouche.com/")
print "beaualalouche - complete"
importBlogToDB("corpus2_dates/xcleacuisine/",cnx,"cleacuisine","www.cleacuisine.fr/")
print "cleacuisine - complete"
importBlogToDB("corpus2_dates/xcoupleofpixels/",cnx,"coupleofpixels","coupleofpixels.fr/")
print "coupleofpixels - complete"
importBlogToDB("corpus2_dates/xdesrecettesagogo/",cnx,"desrecettesagogo","des-recettes-a-gogo.com/")
print "desrecettesagogo - complete"
importBlogToDB("corpus2_dates/xfrancoischarlet/",cnx,"francoischarlet","https://francoischarlet.ch/")
print "francoischarlet - complete"
importBlogToDB("corpus2_dates/xjohncouscous/",cnx,"johncouscous","www.johncouscous.com/")
print "johncouscous - complete"
importBlogToDB("corpus2_dates/xjournaldugamer/",cnx,"journaldugamer","www.journaldugamer.com/")
print "journaldugamer - complete"
importBlogToDB("corpus2_dates/xjulsa/",cnx,"julsa","www.julsa.fr/")
print "julsa - complete"
importBlogToDB("corpus2_dates/xjurilexblog/",cnx,"jurilexblog","www.jurilexblog.com/")
print "jurilexblog - complete"
importBlogToDB("corpus2_dates/xlagourmandiseselonangie/",cnx,"lagourmandiseselonangie","www.la-gourmandise-selon-angie.com/")
print "lagourmandiseselonangie - complete"
importBlogToDB("corpus2_dates/xparalipomenes/",cnx,"paralipomenes","www.paralipomenes.net/")
print "paralipomenes - complete"
importBlogToDB("corpus2_dates/xpechedegourmand/",cnx,"pechedegourmand","pechedegourmand.canalblog.com/")
print "pechedegourmand - complete"
importBlogToDB("corpus2_dates/xphilippebilger/",cnx,"philippebilger","www.philippebilger.com/")
print "philippebilger - complete"
importBlogToDB("corpus2_dates/xroxarmy/",cnx,"roxarmy","roxarmy.com/")
print "roxarmy - complete"
importBlogToDB("corpus2_dates/xtoutchilink/",cnx,"toutchilink","toutchilink.com/")
print "toutchilink - complete"

importBlogToDB("corpus2_dates/xdomotique34/",cnx,"domotique34","http://domotique34.com/")
print "domotique34 - complete"

importBlogToDB("corpus2_dates/xmaisonetdomotique/",cnx,"maisonetdomotique","www.maison-et-domotique.com/")
print "maisonetdomotique - complete"

importBlogToDB("corpus2_dates/xprendreuncafe/",cnx,"prendreuncafe","prendreuncafe.com/blog/")
print "prendreuncafe - complete"

importBlogToDB("corpus2_dates/xshots/",cnx,"shots","www.shots.fr")
print "shots - complete"

importBlogToDB("corpus2_dates/xdomadoo/",cnx,"domadoo","www.domadoo.fr/")
print "domadoo - complete"

#cursor1.execute("select idblog from blog where idblog=13;")
#print cursor1.fetchall()
#close connection
cnx.close()