[User](https://dev.twitter.com/overview/api/users)
 |
 |-- followers_count	Int 		
 |		The number of followers this account currently has. Under certain conditions of duress, this field will temporarily indicate “0.”
 |
 |-- friends_count		Int 		
 |		The number of users this account is following (AKA their “followings”). Under certain conditions of duress, this field will 
 |		temporarily indicate “0.”
 |
 |-- id 				INT64		
 |		The integer representation of the unique identifier for this User. This number is greater than 53 bits and some programming 
 |		languages may have difficulty/silent defects in interpreting it. Using a signed 64 bit integer for storing this identifier 
 |		is safe. Use id_str for fetching the identifier to stay on the safe side. 
 |
 |-- id_str 			String 	
 |		The string representation of the unique identifier for this User. Implementations should use this rather than the large, 
 |		possibly un-consumable integer in id.
 |
 |-- listed_count 		Int 		
 |		The number of public lists that this user is a member of.
 |
 |-- notifications 		Boolean 	
 |		Nullable. Deprecated. May incorrectly report “false” at times. Indicates whether the authenticated user has chosen to receive 
 |		this user’s tweets by SMS.
 |-- protected 			Boolean 	
 |		When true, indicates that this user has chosen to protect their Tweets. 
 |		See [About Public and Protected Tweets](https://support.twitter.com/articles/14016-about-public-and-protected-tweets).
 |		
 |-- screen_name 		String 	
 |		The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject to change. 
 |		Use id_str as a user identifier whenever possible. Typically a maximum of 15 characters long, but some historical accounts 
 |		may exist with longer names.
 |
 |-- status				[Tweets](https://dev.twitter.com/overview/api/tweets)
 |		Nullable. If possible, the user’s most recent tweet or retweet. In some circumstances, this data cannot be provided and this
 |		field will be omitted, null, or empty. Perspectival attributes within tweets embedded within users cannot always be relied upon. 
 |		[See Why are embedded objects stale or inaccurate?](https://dev.twitter.com/docs/faq/basics/why-are-embedded-objects-stale-or-inaccurate).
 |
 |-- statuses_count 	Int
 |		The number of tweets (including retweets) issued by the user.
 |
 |-- time_zone			String
 |
 |-- utc_offset			Int


 status

```
 "status": {
    "coordinates": null,
    "favorited": false,
    "truncated": false,
    "created_at": "Tue Apr 17 16:38:18 +0000 2012",
    "id_str": "192290904646754304",
    "entities": {
      "urls": [
 
      ],
      "hashtags": [
 
      ],
      "user_mentions": [
        {
          "name": "Micah McVicker",
          "id_str": "166661446",
          "id": 166661446,
          "indices": [
            0,
            14
          ],
          "screen_name": "MicahMcVicker"
        }
      ]
    },
    "in_reply_to_user_id_str": "166661446",
    "contributors": null,
    "text": "@MicahMcVicker make sure you're using include_rts=true and no other filters, then walking your timeline by since_id and max_id",
    "retweet_count": 0,
    "in_reply_to_status_id_str": "192290470427246594",
    "id": 192290904646754304,
    "geo": null,
    "retweeted": false,
    "in_reply_to_user_id": 166661446,
    "place": null,
    "in_reply_to_screen_name": "MicahMcVicker",
    "source": "<a href="http://sites.google.com/site/yorufukurou/">YoruFukurou</a>",
    "in_reply_to_status_id": 192290470427246594
  },
```