import tweepy


def get_tweets(twitter_handle, *number_tweets):
    number_tweets = 10
    #  Keys
    consumer_key = 'HXsLvWs59wM1d1XGE7LJQOigJ'
    consumer_secret = 'qBeTcrfx4pzUC0EhNdYco0tQkYKVkhIIebdNr4FB6t7pOYMMoT'
    access_token = '255953036-hY9jLN886BikD0qOBODFgaJ54xwTuAKFBgwXknLB'
    access_secret = 'nXtasuKhZnAcA3djmj5JOrjACa7JsJthuu4amegKn4Eqt'

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
