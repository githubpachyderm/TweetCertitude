import tweepy

CONSUMER_KEY = '00mUio20LllctkuKEImkoEV4G'
CONSUMER_SECRET = 'X2RnfcOkq3Oh3Vo9UxIa3i9sFtSwEGYciKnmS36JTxixA9FLvV'
ACCESS_KEY = '1407746577393881088-KpCkyn1Qs9usPIqoSWCKiHQxMS03xz'
ACCESS_SECRET = '4qpIStfBPC3evCHeFBU6SdFXgkCb8Rt5kHia90dw7ulEn'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

mentions = api.mentions_timeline()

for mention in mentions:
    print(str(mention.id) + ' - ' + mention.text)
    wordList = mention.text.split()
    tweetWordList = []
    searchTermFound = 0
    matchingTweets = []
    rankedMatchingTweets = []
    if '@' in wordList[1]:
        targetAccount = wordList[1]
        if api.search_users(targetAccount):
            potentialHandle = api.search_users(targetAccount)[0].screen_name
            if potentialHandle == targetAccount[1:]:
                #userID = api.search_users(targetAccount)[0].id
                searchTerms = ""
                for word in wordList[2:]:
                    searchTerms = searchTerms + word + " "
                tweets = api.user_timeline(screen_name=potentialHandle, count=200)
                numTweets = len(tweets)
                for tweet in tweets:
                    if searchTerms.lower() in tweet.text.lower():
                        searchTermFound += 1
                        matchingTweets.append(tweet)
                for tweet in matchingTweets:
                    if (tweet.favorite_count > 0):
                        #rankedMatchingTweets.append(tweets.index(tweet.favorite_count))
                        matchingTweets.sort(key=lambda tweet: tweet.favorite_count, reverse=True)

                if len(matchingTweets) >= 3:
                    originalID = mention.id
                    intro1 = searchTerms + "has been mentioned in " + str(searchTermFound) + " tweets out of " + str(numTweets) + " tweets."
                    intro2 = "\nTop 3 most liked matching tweets: "
                    for tweet in matchingTweets[0:3]:
                        reply = potentialHandle + " : " + tweet.text + ", " + str(tweet.favorite_count)
                        api.update_status(status=reply, in_reply_to_status_id=originalID, auto_populate_reply_metadata=True)
                    #api.update_status(status=("@" + mention.user.name + " " + intro1+intro2+reply), in_reply_to_status_id=originalID)
                    api.update_status(status=reply, in_reply_to_status_id=originalID, auto_populate_reply_metadata=True)

            else:
                print("no match")
        else:
            print("account not found")


#print("this is my twitter bot")
