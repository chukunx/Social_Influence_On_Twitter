# Documentation

## [REST APIs](https://dev.twitter.com/rest/public)

The REST APIs provide programmatic access to read and write Twitter data. Author a new Tweet, read author profile and follower data, and more. The REST API identifies Twitter applications and users using OAuth; responses are available in JSON.

### [API Rate Limits](https://dev.twitter.com/rest/public/rate-limiting)

#### 15 Minute Windows

Rate limits in version 1.1 of the API are divided into 15 minute intervals, which is a change from the 60 minute blocks in version 1.0. 

While in version one of the API, an OAuth-enabled application could initiate 350 GET-based requests per hour per access token, API v1.1’s rate limiting model allows for a wider ranger of requests through per-method request limits. There are two initial buckets available for GET requests: 15 calls every 15 minutes, and 180 calls every 15 minutes. 

#### GET and POST Request Limits

Rate limits on “reads” from the system are defined on a per user and per application basis, while rate limits on writes into the system are defined solely at the user level. 

Contrast this with write allowances, which are defined on a per user basis. So if user A ends up posting 5 Tweets with application Z, then for that same period, regardless of any other application that user A opens, those 5 POSTs will count against any other application acting on behalf of user A during that same window of time.

Lastly, there may be times in which the rate limit values that we return are inconsistent, or cases where no headers are returned at all. Perhaps memcache has been reset, or one memcache was busy so the system spoke to a different instance: the values may be inconsistent now and again. We will make a best effort to maintain consistency, but we will err toward giving an application extra calls if there is an inconsistency.

#### Blacklisting

We ask that you honor the rate limit. If you or your application abuses the rate limits we will blacklist it. If you are blacklisted you will be unable to get a response from the Twitter API. If you or your application has been blacklisted and you think there has been an error you can contact the email address on our [Support](https://dev.twitter.com/docs/support) page. So we can get you back online quickly please include the following information:

1. If you are using the REST API, make a call to the [GET application / rate_limit_status](https://dev.twitter.com/rest/reference/get/application/rate_limit_status) from the account or computer which you believe to be blacklisted.
2. Explain why you think your application was blacklisted.
3. Describe in detail how you have fixed the problem that you think caused you to be blacklisted.

### [Public API](https://dev.twitter.com/rest/public)

#### [The Search API](https://dev.twitter.com/rest/public/search)

The Twitter Search API is part of Twitter’s v1.1 REST API. It allows queries against the indices of recent or popular Tweets and behaves similarily to, but not exactly like the Search feature available in Twitter mobile or web clients, such as Twitter.com search.

Before getting involved, it’s important to know that the Search API is focused on relevance and not completeness. This means that some Tweets and users may be missing from search results. If you want to match for completeness you should consider using a Streaming API instead.

A detailed reference on this API endpoint can be found at [GET search/tweets](https://dev.twitter.com/rest/reference/get/search/tweets).

#### [Rate Limits: Chart](https://dev.twitter.com/rest/public/rate-limits)

#### [GET friends/ids](https://dev.twitter.com/rest/reference/get/friends/ids)

Returns a cursored collection of user IDs for every user the specified user is following (otherwise known as their “friends”).

At this time, results are ordered with the most recent following first — however, this ordering is subject to unannounced change and eventual consistency issues. Results are given in groups of 5,000 user IDs and multiple “pages” of results can be navigated through using the `next_cursor` value in subsequent requests. See [Using cursors to navigate collections](https://dev.twitter.com/overview/api/cursoring) for more information.

This method is especially powerful when used in conjunction with [GET users / lookup](https://dev.twitter.com/rest/reference/get/users/lookup), a method that allows you to convert user IDs into full [user objects](https://dev.twitter.com/overview/api/users) in bulk.

#### [GET followers/ids](https://dev.twitter.com/rest/reference/get/followers/ids)

#### [GET friends/list](https://dev.twitter.com/rest/reference/get/friends/list)

Returns a cursored collection of user objects for every user the specified user is following (otherwise known as their “friends”).

#### [GET followers/list](https://dev.twitter.com/rest/reference/get/followers/list)

#### [GET users/lookup](https://dev.twitter.com/rest/reference/get/users/lookup)

Returns fully-hydrated user objects for up to 100 users per request, as specified by comma-separated values passed to the user_id and/or screen_name parameters.

This method is especially useful when used in conjunction with collections of user IDs returned from [GET friends / ids](https://dev.twitter.com/rest/reference/get/friends/ids) and [GET followers / ids](https://dev.twitter.com/rest/reference/get/followers/ids).

[GET users / show](https://dev.twitter.com/rest/reference/get/users/show) is used to retrieve a single user object.

There are a few things to note when using this method.

* You must be following a protected user to be able to see their most recent status update. If you don’t follow a protected user their status will be removed.
* The order of user IDs or screen names may not match the order of users in the returned array.
* If a requested user is unknown, suspended, or deleted, then that user will not be returned in the results list.
* If none of your lookup criteria can be satisfied by returning a user object, a HTTP 404 will be thrown.
* You are strongly encouraged to use a POST for larger requests.

Returns a cursored collection of user IDs for every user following the specified user.

#### [GET users/show](https://dev.twitter.com/rest/reference/get/users/show)

Returns a [variety of information](https://dev.twitter.com/overview/api/users) about the user specified by the required  `user_id` or `screen_name` parameter. The author’s most recent Tweet will be returned inline when possible.

[GET users / lookup](https://dev.twitter.com/rest/reference/get/users/lookup) is used to retrieve a bulk collection of user objects.

You must be following a protected user to be able to see their most recent Tweet. If you don’t follow a protected user, the users Tweet will be removed. A Tweet will not always be returned in the `current_status` field.

# [API Overview](https://dev.twitter.com/overview/api)

## [Object: User](https://dev.twitter.com/overview/api/users)

| FIELD            | TYPE      | DESCRIPTION |
| :--------------- |:--------- |:----------- |
|`followers_count` | `Int`     | The number of followers this account currently has. Under certain conditions of duress, this field will temporarily indicate “0.” |
|`friends_count`   | `Int`     | The number of users this account is following (AKA their “followings”). Under certain conditions of duress, this field will temporarily indicate “0.”|
|`id`              | `INT64`   | The integer representation of the unique identifier for this User. This number is greater than 53 bits and some programming languages may have difficulty/silent defects in interpreting it. Using a signed 64 bit integer for storing this identifier is safe. Use id_str for fetching the identifier to stay on the safe side. |
|`id_str`          | `String`  | The string representation of the unique identifier for this User. Implementations should use this rather than the large possibly un-consumable integer in id.|
|`listed_count `   | `Int`     | The number of public lists that this user is a member of.|
|`notifications`   | `Boolean` | *Nullable*. Deprecated. May incorrectly report “false” at times. Indicates whether the authenticated user has chosen to receive this user’s tweets by SMS.|
|`protected`       | `Boolean` |When true, indicates that this user has chosen to protect their Tweets. See [About Public and Protected Tweets](https://support.twitter.com/articles/14016-about-public-and-protected-tweets).|
|`screen_name`     | `String`  | The screen name, handle, or alias that this user identifies themselves with. screen_names are unique but subject to change. Use id_str as a user identifier whenever possible. Typically a maximum of 15 characters long, but some historical accounts may exist with longer names.|
|`status`          | [`Tweets`](https://dev.twitter.com/overview/api/tweets) | *Nullable*. If possible, the user’s most recent tweet or retweet. In some circumstances, this data cannot be provided and this field will be omitted, null, or empty. Perspectival attributes within tweets embedded within users cannot always be relied upon. [See Why are embedded objects stale or inaccurate?](https://dev.twitter.com/docs/faq/basics/why-are-embedded-objects-stale-or-inaccurate).|
|`statuses_count`  | `Int`     | The number of tweets (including retweets) issued by the user.|
|`default_profile_image`|`Boolean`|When true, indicates that the user has not uploaded their own avatar and a default egg avatar is used instead.|
|`created_at`|`String`|The UTC datetime that the user account was created on Twitter.|
|`time_zone`       | `String`  |*Nullable*. A string describing the Time Zone this user declares themselves within.|
|`utc_offset`      | `Int`     |*Nullable*. The offset from GMT/UTC in seconds.|

## [Object: Twitter](https://dev.twitter.com/overview/api/tweets)

| FIELD            | TYPE      | DESCRIPTION |
| :--------------- |:--------- |:----------- |
|`created_at`      |`String`   |UTC time when this Tweet was created.|
|`current_user_retweet`|`Object`|*Perspectival*. Only surfaces on methods supporting the `include_my_retweet` parameter, when set to true. Details the Tweet ID of the user’s own retweet (if existent) of this Tweet.[discussion](https://twittercommunity.com/t/current-user-retweet-absent-in-retweeted-status/8360)|
|`favorite_count`  |`Integer`  |*Nullable*. Indicates approximately how many times this Tweet has been “liked” by Twitter users.|
|`id_str`          |`String`   |The string representation of the unique identifier for this Tweet. Implementations should use this rather than the large integer in id.|
|`in_reply_to_status_id_str`|`String`|*Nullable*. If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s ID.|
|`in_reply_to_user_id_str`|`String`|*Nullable*. If the represented Tweet is a reply, this field will contain the integer representation of the original Tweet’s author ID. This will not necessarily always be the user directly mentioned in the Tweet.|
|`quoted_status_id_str`|`String`|This field only surfaces when the Tweet is a quote Tweet. This is the string representation Tweet ID of the quoted Tweet.|
|`quoted_status`   |[`Tweet`](https://dev.twitter.com/overview/api/tweets)|This field only surfaces when the Tweet is a quote Tweet. This attribute contains the Tweet object of the original Tweet that was quoted.|
|`retweet_count`   |`Int`      |Number of times this Tweet has been retweeted. This field is no longer capped at 99 and will not turn into a String for “100+” Thank god😂|
|`retweeted_status`|[`Tweet`](https://dev.twitter.com/overview/api/tweets)|Users can amplify the broadcast of tweets authored by other users by retweeting. Retweets can be distinguished from typical Tweets by the existence of a retweeted_status attribute. This attribute contains a representation of the original Tweet that was retweeted. Note that retweets of retweets do not show representations of the intermediary retweet, but only the original tweet. (Users can also unretweet a retweet they created by deleting their retweet.)|
|`user`|[`Users`](https://dev.twitter.com/overview/api/users)|The user who posted this Tweet. Perspectival attributes embedded within this object are unreliable. [See Why are embedded objects stale or inaccurate?](https://dev.twitter.com/docs/faq/basics/why-are-embedded-objects-stale-or-inaccurate).|

## [Object: Entities](https://dev.twitter.com/overview/api/entities)


## Samples

### `status` 
 
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

### `current_user_retweet`

```
"current_user_retweet": {
  "id": 26815871309,
  "id_str": "26815871309"
}
```

# Other useful information

1. [Twitter: Why the different types of retweet?](http://joelhughes.com/2013/02/23/twitter-types-of-retweet/)
2. [Twitter for Websites](https://dev.twitter.com/web/overview) is a suite of embeddable widgets, buttons, and client-side scripting tools to integrate Twitter and display Tweets on your website or JavaScript application, including a single Tweet, multiple Tweets, Twitter Moments, Tweet Button, and the Follow Button.
3. Twitter [Cards](https://dev.twitter.com/cards/overview) display additional content alongside a Tweet for supported links. Highlight a photo, video, or other page summary when your links are shared on Twitter to drive additional traffic to your website, iOS, or Android app. 
