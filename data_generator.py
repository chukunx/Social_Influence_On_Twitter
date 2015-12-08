import sqlite3 as lite
import simplejson as json
import time 
import urllib
import os
import sys

from klout import *

directoryForDB = "./data/"
if not os.path.exists(directoryForDB):  # create a new one if it is not exist 
	print "Wrong directory."
	
directoryForDB = directoryForDB + "temp10000.db"
con = lite.connect(directoryForDB)

# userScore = {}
with con:
	cur = con.cursor()
	selectStatement = 'SELECT * FROM users'
	users = cur.execute(selectStatement).fetchall()
	con.commit()
	# fo = open("./data/twitter5.arff", "w")
	fo = open("./data/twitter5.txt", "w")
	count = 0
	for user in users:
		print count
		count = count + 1
		rank = int(user[2])/10
		if rank < 2:
			ranking = 1
		elif rank < 4:
			ranking = 2
		elif rank < 6:
			ranking = 3
		elif rank < 8:
			ranking = 4
		else:
			ranking = 5
		# fo.write("%d,%d,%d,%d,%d,%d,%d\n" % (ranking,user[3],user[4],user[5],user[6],user[7],user[8]))
		fo.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\n" % (ranking,user[3],user[4],user[5],user[6],user[7],user[8]))
		# print type(user[2])
	fo.close()
con.close()
