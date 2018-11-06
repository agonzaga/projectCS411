import tweepy
import sqlite3


def create_table():
    # Create table
    c.execute('''CREATE TABLE tweets (Name text, tweets text)''')
    return 0

def insert_into_table(twitter_handle, tweets_list):
    # Insert a row of data
    for item in tweets_list:
        c.execute("INSERT INTO tweets (Name, tweets) values (?, ?)", (twitter_handle, item))
    return 0

def close_db():
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return 0


def read_db():
    c.execute('SELECT * FROM tweets')
    print(c.fetchone())
    return 0



def get_tweets(twitter_handle, *number_tweets):
    global conn 
    global c
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    number_tweets = 30
    #  Keys
    consumer_key = 'none'
    consumer_secret = 'none'
    access_token = 'none'
    access_secret = 'none'

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


    # SQL
    #create_table()
    #insert_into_table(twitter_handle, tweets_list)
    read_db()
    close_db()

    return tweets_list


if __name__ == '__main__':
    get_tweets('neiltyson', 5)
