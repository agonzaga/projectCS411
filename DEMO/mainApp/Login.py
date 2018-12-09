from flask_oauthlib.client import OAuth
from flask import request, redirect,session, url_for, flash
twitter_acc = None
def login_twitter():
    print("OAUTH STARTED")
    oauth = OAuth()

    # Use Twitter as example remote application
    twitter = oauth.remote_app('twitter',
    # unless absolute urls are used to make requests, this will be added
    # before all URLs.  This is also true for request_token_url and others.
    base_url='https://api.twitter.com/1/',
    # where flask should look for new request tokens
    request_token_url='https://api.twitter.com/oauth/request_token',
    # where flask should exchange the token with the remote application
    access_token_url='https://api.twitter.com/oauth/access_token',
    # twitter knows two authorizatiom URLs.  /authorize and /authenticate.
    # they mostly work the same, but for sign on /authenticate is
    # expected because this will give the user a slightly different
    # user interface on the twitter side.
    authorize_url='https://api.twitter.com/oauth/authenticate',
    # the consumer keys from the twitter application registry.
    consumer_key='HXsLvWs59wM1d1XGE7LJQOigJ',
    consumer_secret='qBeTcrfx4pzUC0EhNdYco0tQkYKVkhIIebdNr4FB6t7pOYMMoT'
    )
    twitter_acc = twitter

    @twitter.tokengetter
    def get_twitter_token(token=None):
        return session.get('twitter_token')

    twitter.authorize(callback=url_for('oauth_authorized',
    next=request.args.get('next') or request.referrer or None))

def oauth():
    next_url = request.args.get('next') or url_for('index')
    resp = twitter_acc.authorized_response()
    if resp is None:
            flash(u'You denied the request to sign in.')
            return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
        )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)