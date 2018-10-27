import tweepy


def get_tweets(twitter_handle, *number_tweets):
    number_tweets = 30
    #  Keys

    # Authorization
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    # Gathering twitter data
    try:
        tweets = api.user_timeline(screen_name=twitter_handle,          # Gather first set of tweets
                                   count=number_tweets, include_rts=False,
                                   exclude_replies=True)
    except:
        print('The given username does not exist. \n')
        return 0

    tweets_list = []
    for item in tweets:
        tweets_list.append(item.text)

    print(tweets_list)
    return tweets_list
