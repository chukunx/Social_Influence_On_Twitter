import oauth2 as oauth
import sqlite3 as lite
import simplejson as json
import time 
import urllib
import os

############################## Authentication ##############################

############################## Authentication ##############################

# Request for user information from twitter.
def requestForUserInfo(client, user_id):
	# 180 requests / 15 min
	print "\n%s: Requesting user information ..." % user_id
	url = """https://api.twitter.com/1.1/users/show.json?user_id=%s""" % user_id 
	header, fhand = client.request(url, method="GET")
	userEntity = json.loads(fhand, encoding='utf8')

	# Basic infor of the seed.
	user = {}
	user['id_str'] = userEntity['id_str']
	user['screen_name'] = userEntity['screen_name']
	user['followers_count'] = userEntity['followers_count']
	user['friends_count'] = userEntity['friends_count']
	user['statuses_count'] = userEntity['statuses_count']
	user['created_at'] = userEntity['created_at']
	user['default_profile_image'] = userEntity['default_profile_image'] ## When true, indicates that the user has not uploaded their own avatar and a default egg avatar is used instead.

	# 300 requests / 15 min
	print " * %s: Calculating fa and re ... " % user_id
	url = """https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=%s&trim_user=true&exclude_replies=true&include_rts=false&count=10""" % user_id
	header, fhand = client.request(url, method="GET")
	twitters = json.loads(fhand, encoding='utf8')

	twitterCount = len(twitters)
	if(twitterCount == 0):
		user['favorite_count'] = 0
		user['retweet_count'] = 0
	else:
		totalFavorite = 0
		totalRetweet = 0
		for twitter in twitters:
			totalRetweet = totalRetweet + twitter['retweet_count']
			totalFavorite = totalFavorite + twitter['favorite_count']
		user['favorite_count'] = totalFavorite/twitterCount
		user['retweet_count'] = totalRetweet/twitterCount
	return user
	
def requestForRelations(client, user_id, requestType):
	ids = []
	cursor = -1
	# 15 requests / 15 min  
	print " * %s: Requesting for %s relations from twitter." % (user_id, requestType)
	url = """https://api.twitter.com/1.1/%s/ids.json?&user_id=%s&stringify_ids=true""" % (requestType, user_id) 
	url_with_cursor = url + "&cursor=" + str(cursor)
	header, fhand = client.request(url_with_cursor, method="GET")
	tempIds = json.loads(fhand, encoding='utf8')
	ids = tempIds['ids']
	cursor = tempIds['next_cursor']
	while(cursor != 0):
		url_with_cursor = url + "&cursor=" + str(cursor)
		header, fhand = client.request(url_with_cursor, method="GET")
		tempIds = json.loads(fhand, encoding='utf8')
		ids.extend(tempIds['ids'])
		cursor = tempIds['next_cursor']
	return ids

def insertNewUser(con, user):
	cur = con.cursor()
	print " * Inserting %s ... " % user['id_str']
	insertNewUser = 'INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?)'
	flag = 0
	if(user['default_profile_image']):
		flag = 1
	parms = (user['id_str'], user['screen_name'], None, user['followers_count'], user['friends_count'], user['retweet_count'] ,user['favorite_count'], user['statuses_count'], flag, user['created_at'])
	cur.execute(insertNewUser, parms)
	con.commit()

def waitToCross(seconds, start):
	print "API Limitation: Wait for %d seconds." % seconds
	overlap = time.time()-start
	count = 0;
	while(overlap < seconds):
		overlap = time.time()-start
	return time.time()

# time controler
timeUserInfor = time.time()
timeRelation = timeUserInfor

# Create tables.
directoryForDB = "./data/"
if not os.path.exists(directoryForDB):  # create a new one if it is not exist 
	os.makedirs(directoryForDB)
	
directoryForDB = directoryForDB + "twitter.db"
con = lite.connect(directoryForDB)
with con:
	cur = con.cursor()
	# cur.execute("DROP TABLE IF EXISTS users") 
	# cur.execute("DROP TABLE IF EXISTS friends") 
	# cur.execute("DROP TABLE IF EXISTS followers")
	# cur.execute("CREATE TABLE users(user_id TEXT, screen_name TEXT, klout_score NUMERIC, followers_count INTEGER, friends_count INTEGER, retweet_count NUMERIC, favorite_count NUMERIC, statuses_count INTEGER, default_profile_image INTEGER, user_created_at TEXT)")
	# cur.execute("CREATE TABLE friends(user_id TEXT, friends_id TEXT)")
	# cur.execute("CREATE TABLE followers(user_id TEXT, followers_id TEXT)")
	# con.commit()

	# [console](https://dev.twitter.com/rest/tools/console)
	seedUsers = {'633660653':'JazmeenStyle'}
	# seedUsers = {'1143566300':'aolivex','37505751':'MakaylaAWray','1018277820':'Fotofilmic'}
	# seedUsers = {'328860549':'makili1949','2981527257':'TraceyWCDC','3538939877':'ashplantus'}

	count = {'countSeed':0, 'countTotal':0}
	
	for seedId in seedUsers:
		# Request for seed user's information.
		timeUserInfor = waitToCross(5,timeUserInfor) ######################################
		try:
			user = requestForUserInfo(client_0, seedId)
		except Exception, e:
			print " !!!!! Exception !!!!!! "
			continue
	
		# Request for friends' id list.
		timeRelation = waitToCross(60,timeRelation) ######################################
		try:
			user['friends_ids'] = requestForRelations(client_0, seedId, "friends")
		except Exception, e:
			print " !!!!! Exception !!!!!! "
			continue

		# Request for followers' id list.
		timeRelation = waitToCross(60,timeRelation) ######################################
		try:
			user['followers_ids'] = requestForRelations(client_1, seedId, "followers")
		except Exception, e:
			print " !!!!! Exception !!!!!! "
			continue	
		print ""
	
		relationCount = {'followers':0,'followersRemoved':0,'friends':0,'friendsRemoved':0}
		
		print "Loading user from TABLE(users) ... "
		allIdsInUsers = 'SELECT user_id FROM users'
		theDb = cur.execute(allIdsInUsers).fetchall()
		print " * %d users in total." % len(theDb)
		newId = user['id_str']
		newIdTuple = tuple((user['id_str'].decode('unicode-escape'),))
		if(newIdTuple not in theDb):	
			insertNewUser(con, user)
			theDb.extend(newIdTuple)
			count['countSeed'] += 1
			count['countTotal'] += 1
		else:
			print " * Seed %s omitted." % newId

		print " * %s: Inserting friends into TABLE(friends) ... " % seedId
		for friend in user['friends_ids']:
			insertFriend = 'INSERT INTO friends VALUES(?,?)'
			parms = (newId, friend)
			cur.execute(insertFriend, parms)
			con.commit()
			friendTuple = tuple((friend.decode('unicode-escape'),))
			if(friendTuple not in theDb):
				timeUserInfor = waitToCross(5,timeUserInfor) ######################################
				try:
					theFriend = requestForUserInfo(client_1, friend)
				except Exception, e:
					print " !!!!! Exception !!!!!! "
					continue
				insertNewUser(con,theFriend)
				theDb.extend(friendTuple)
			else:
				relationCount['friendsRemoved'] += 1
				print " * Friend %s omitted." % friend
			count['countTotal'] += 1
			relationCount['friends'] += 1
		print "\n###########################################################################################"
		print "%d frineds @%s have in total, %d friends inserted. %d of friends have been removed." % (user['friends_count'], user['screen_name'], relationCount['friends'], relationCount['friendsRemoved'])
		
		print " * %s: Inserting followers into TABLE(followers) ... " % seedId
		for follower in user['followers_ids']:
			insertFollower = 'INSERT INTO followers VALUES(?,?)'
			parms = (newId, follower)
			cur.execute(insertFollower, parms)
			followerTuple = tuple((follower.decode('unicode-escape'),))
			if(followerTuple not in theDb):
				timeUserInfor = waitToCross(5,timeUserInfor) ######################################
				try:
					theFollower = requestForUserInfo(client_0, follower)
				except Exception, e:
					print " !!!!! Exception !!!!!! "
					continue
				insertNewUser(con,theFollower)
				theDb.extend(followerTuple)
			else:
				relationCount['followersRemoved'] += 1
				print " * Follower %s omitted." % follower
			count['countTotal'] += 1
			relationCount['followers'] += 1
		print "\n###########################################################################################"
		print "%d followers @%s have in total, %d followers inserted.%d of followers have been removed." % (user['followers_count'], user['screen_name'], relationCount['followers'], relationCount['followersRemoved'])
con.close()
	