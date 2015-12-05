import oauth2 as oauth
import sqlite3 as lite
import simplejson as json
import urllib
import os

############################## Authentication ##############################

############################## Authentication ##############################

# [console](https://dev.twitter.com/rest/tools/console)
# seedUsers = {'1746891':'ninaksimon','59268383','STurkle'}

seedUsers = {'1143566300':'aolivex'}

count = {countSeed:0, countTotal:0}

for seedId in seedUsers:
	# Request for seed user's information.
	user = requestForUserInfo(client_0, seedId)

	# Request for friends' id list.
	user['friends_ids'] = requestForRelations(client_0, seedId,"friends")

	# Request for followers' id list.
	user['followers_ids'] = requestForRelations(client_1, seedId,"followers")

	# Insert INTEGERo database.
	directoryForDB = "./data"
	if not os.path.exists(directoryForDB):  # create a new one if it is not exist 
		os.makedirs(directoryForDB)
	
	directoryForDB = directoryForDB + "twitter.db"
	con = lite.connect(directoryForDB)
	### open a connection to store the data
	with con:
		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS users") 
		cur.execute("DROP TABLE IF EXISTS friends") 
		cur.execute("DROP TABLE IF EXISTS followers")
		cur.execute("CREATE TABLE users(user_id TEXT, screen_name TEXT, klout_score INTEGER, followers_count INTEGER, friends_count INTEGER, retweet_count NUMERIC, favorite_count NUMERIC, statuses_count INTEGER, default_profile_image INTEGER, user_created_at TEXT)")
		cur.execute("CREATE TABLE friends(user_id TEXT, friends_id TEXT)")
		cur.execute("CREATE TABLE followers(user_id TEXT, followers_id TEXT)")
		
		relationCount = {'followers':0,'followersRemoved':0,'friends':0,'friendsRemoved':0}
		
		print "Loading user from TABLE users ... \n"
		allIdsInUsers = 'SELECT user_id FROM users'
		theDb = cur.execute(allIdsInUsers)
		print "\t%d users in total.\n" % len(theDb)

		newId = user['id_str']
		if(newId not in theDb):
			insertNewUser(cur, user).fetchall()
			theDb.extend(newId)
			count['countSeed'] += 1
			count['countTotal'] += 1

			print "Inserting users %s is following into TABLE friends ... \n" % seedId
			for friend in user['friends_ids']:
				insertFriend = 'INSERT INTO friends VALUES(?,?)'
				parms = (newId, friend)
				cur.execute(insertFriend, parms)
				if(friend not in theDb):
					theFriend = requestForUserInfo(client_1, friend)
					insertNewUser(cur,theFriend).fetchall()
					theDb.extend(theFriend['id_str'])
				else:
					relationCount['friendsRemoved'] += 1
				count['countTotal'] += 1
				relationCount['friends'] += 1
			print "\t%d frineds @%s have in total, %d friends inserted. %d of friends have been removed.\n" % (user['friends_count'], user['screen_name'], relationCount['friends'], relationCount['friendsRemoved'])

			print "Inserting %s's followers' id into TABLE followers ... \n" % seedId
			for follower in user['followers_ids']:
				insertFollower = 'INSERT INTO followers VALUES(?,?)'
				parms = (newId, follower)
				cur.execute(insertFollower, parms)
				if(follower not in theDb):
					theFollower = requestForUserInfo(client_1, follower)
					insertNewUser(cur,theFollower).fetchall()
					theDb.extend(theFollower['id_str'])
				else:
					relationCount['followersRemoved'] += 1
				count['countTotal'] += 1
				relationCount['followers'] += 1
			print "\t%d followers @%s have in total, %d followers inserted.%d of followers have been removed.\n" % (user['followers_count'], user['screen_name'], relationCount['followers'], relationCount['followersRemoved'])

			

# Request for user information from twitter.
def requestForUserInfo(client, user_id):
	# 180 requests / 15 min
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
	url = """https://api.twitter.com/1.1/statuses/user_timeline.json?user_id=%s&trim_user=true&exclude_replies=true&include_rts=false&count=10""" % user_id
	header, fhand = client_0.request(url, method="GET")
	twitters = json.loads(fhand, encoding='utf8')

	twitterCount = len(twitters)
	totalFavorite = 0
	totalRetweet = 0
	for twitter in twitters:
		totalRetweet += twitter['retweet_count']
		totalFavorite += twitter['favorite_count']

	user['favorite_count'] = totalFavorite/twitterCount
	user['retweet_count'] = totalRetweet/twitterCount
	return user
	
def requestForRelations(client, user_id, requestType):
	ids = []
	cursor = -1
	# 15 requests / 15 min  
	url = """https://api.twitter.com/1.1/%s/ids.json?&user_id=%s&stringify_ids=true""" % (requestType,seedId) 
	url_with_cursor = url + "&cursor=" + cursor
	header, fhand = client.request(url_with_cursor, method="GET")
	tempIds = json.loads(fhand, encoding='utf8')
	ids = tempIds['ids']
	cursor = tempIds['next_cursor']
	while(cursor != 0):
		url_with_cursor = url + "&cursor=" + cursor
		header, fhand = client.request(url_with_cursor, method="GET")
		tempIds = json.loads(fhand, encoding='utf8')
		ids.extend(tempIds['ids'])
		cursor = tempIds['next_cursor']
	return ids

def insertNewUser(cur, user):
	print "Inserting new user '%s' into db ... \n" % user['id_str']
	insertNewUser = 'INSERT INTO users VALUES(?,?,?,?,?,?,?,?,?,?)'
	flag = 0
	if(user['default_profile_image']):
		flag = 1
	parms = (user['id_str'], user['screen_name'], None, user['followers_count'], user['friends_count'], user['retweet_count'] ,user['favorite_count'], user['statuses_count'], flag, user['created_at'])
	cur.execute(insertNewUser, parms)
