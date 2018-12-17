from flask_oauthlib.client import OAuth
from flask import request, redirect, session, url_for, flash
from flask_oauthlib.contrib.apps import twitter

oauth = OAuth()

name= None
# Use Twitter as example remote application
twitter = oauth.remote_app('twitter',
                               # unless absolute urls are used to make requests, this will be added
                               # before all URLs.  This is also true for request_token_url and others.
                               base_url='https://api.twitter.com/1/',
                               # where flask should look for new request tokens
                               request_token_url='https://api.twitter.com/oauth/request_token',
                               # where flask should exchange the token with the remote application
                               access_token_url='https://api.twitter.com/oauth/access_token',
                               # twitter knows two authorization URLs.  /authorize and /authenticate.
                               # they mostly work the same, but for sign on /authenticate is
                               # expected because this will give the user a slightly different
                               # user interface on the twitter side.
                               authorize_url='https://api.twitter.com/oauth/authenticate',
                               # the consumer keys from the twitter application registry.
                               consumer_key='eojCvY0S1BEJXUSMMC2cKH4k5',
                               consumer_secret='9nB0VeYTz3AbJHkvqFsrMf3Rnui358q9BKCGdhuUByRWtqHcMJ'
                               )

def login_twitter():
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.args.get('next') or request.referrer or None))

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')

    # this is causing it to fail



def oauth():
    next_url = url_for('index') #  or request.args.get('next') or
    resp = twitter.authorized_response()
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']
    name = resp['screen_name']
    print("name is: ",name)
    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)
