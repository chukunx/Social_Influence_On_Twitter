import sqlite3 as lite
import simplejson as json
import time 
import urllib
import os

from klout import *

directoryForDB = "./data/"
if not os.path.exists(directoryForDB):  # create a new one if it is not exist 
	print "Wrong directory."
	
directoryForDB = directoryForDB + "twitter.db"
con = lite.connect(directoryForDB)

# userScore = {}
with con:
	cur = con.cursor()
	selectStatement = 'SELECT screen_name FROM users WHERE klout_score IS NULL'
	users = cur.execute(selectStatement).fetchall()

	k = Klout('8q57psabzxuaxdz6pdsj7rng', secure=True)

	count = 1
	noScore = 0
	for u in users:
		screen_name = u[0]
		try:
			print "%d. User: %s." % (count,screen_name)
			count = count + 1
			kloutId = k.identity.klout(screenName=screen_name).get('id')
			score = k.user.score(kloutId=kloutId).get('score')
		except Exception, e:
			print " !!!!! No score !!!!! "
			noScore = noScore + 1
			continue
		else:
			# userScore[user] = score
			print " * score: %f" % score
			cur.execute("UPDATE users SET klout_score = ? WHERE screen_name = ? ", (score, screen_name))
			con.commit()
con.close()
print "\n###########################################################################################"
print "%d users requested, %d scores inserted, %d scores missing." % (len(users),count,noScore)
