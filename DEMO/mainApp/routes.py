from flask import render_template, request, session, redirect
from mainApp import app, twitterCall, watsonCall, Login, validateInput
import requests
import json
import sqlite3
import random
from flask_oauthlib.client import OAuth
from flask import request, redirect, session, url_for, flash


@app.route('/')
@app.route('/index')
def index():
    names = [("Wei-Ning Chen", "cweining@bu.edu"), ("Harry Feng", "hfeng125@bu.edu"), ("Andre Gonzaga", "agonzaga@bu.edu"),
             ("Chichiger Shyy", "cshyy@bu.edu")]
    random.shuffle(names)
    userName = Login.getName()
    return render_template('index.html', userName=userName, names=names)


@app.route('/getTweet')
def getTweetHtml():
    userName = Login.getName()
    return render_template('getTweet.html', userName=userName)


@app.route('/processLogin')
def processLogin():
    render_template('login.html')
    test = Login.get_twitter_token()
    return Login.login_twitter()


@app.route('/oauth_authorized')
def oauth_authorized():
    render_template('oauth_authorized.html')
    return Login.oauth()


@app.route('/displayPersonality')
def analyzeMe():
    userName = Login.getName()
    if(userName != None):
        ret = twitterCall.get_tweets(userName)

        # Remove URL text from tweets
        pretty = validateInput.prettyTweets(ret)
        d = pretty[0]
        tweetsAsString = pretty[1]

        # Checks to see if Twitter User has enough tweets [Watson requires min of 100 words]
        if(len(tweetsAsString.split()) < 100):
            return render_template('getTweet.html', userName=userName, status=True, msg='You do not have enough tweets required to be analyzed.')

        with open("profile.json", "w") as file:
            file.write(json.dumps(d))

        traits = watsonCall.getWatsonAnalysis()

        traitPercentile = watsonCall.formatAnalysis(traits)

        twitterCall.drop_table()
        twitterCall.close_db()

        return render_template('displayPersonality.html', userName=userName, listOfTweets=traitPercentile, user=userName)

    else:
        return redirect("/", code=302)


@app.route('/displayPersonality', methods=['POST'])
def displayTweets():
    userName = Login.getName()
    tweets = request.form["twitter"]
    ret = twitterCall.get_tweets(tweets)

    if(ret == 0):
        return render_template('getTweet.html', userName=userName, status=True, msg='The given username does not exist.')

    # Remove URL text from tweets
    pretty = validateInput.prettyTweets(ret)
    d = pretty[0]
    tweetsAsString = pretty[1]

    # Checks to see if Twitter User has enough tweets [Watson requires min of 100 words]
    if(len(tweetsAsString.split()) < 100):
        return render_template('getTweet.html', userName=userName, status=True, msg='The user does not have enough tweets required to be analyzed.')

    with open("profile.json", "w") as file:
        file.write(json.dumps(d))

    traits = watsonCall.getWatsonAnalysis()

    traitPercentile = watsonCall.formatAnalysis(traits)

    twitterCall.drop_table()
    twitterCall.close_db()

    return render_template('displayPersonality.html', userName=userName, listOfTweets=traitPercentile, user=tweets)
