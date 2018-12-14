from flask import render_template, request, session, redirect
from mainApp import app, twitterCall, watsonCall, Login
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
    return render_template('index.html', names=names)


@app.route('/getTweet')
def getTweetHtml():
    return render_template('getTweet.html')


@app.route('/login') #i don't think this is getting used
def login():
    return render_template('login.html')


@app.route('/processLogin')
def processLogin():
    return render_template('login.html')
    #return Login.login_twitter()

@app.route('/oauth_authorized')
def oauth_authorized():
    return render_template('oauth_authorized.html')
    #return Login.oauth()


@app.route('/displayPersonality', methods=['POST'])
def displayTweets():
    tweets = request.form["twitter"]
    ret = twitterCall.get_tweets(tweets)

    if(ret == 0):
        return render_template('getTweet.html', status=True, msg='The given username does not exist.')

    # Remove URL text from tweets
    d = {"contentItems": []}
    tweetsAsString = ""
    for item in ret:
        if ("https://" in item or "http://" in item):
            item = item[:item.find("http")]
        d["contentItems"].append({"content": item})
        tweetsAsString += item + " "

    # Checks to see if Twitter User has enough tweets [Watson requires min of 100 words]
    if(len(tweetsAsString.split()) < 100):
        return render_template('getTweet.html', status=True, msg='The user does not have enough tweets required to be analyzed.')

    with open("profile.json", "w") as file:
        file.write(json.dumps(d))

    traits = []
    watson_text = watsonCall.watson("../profile.json")
    watson_text2 = json.loads(watson_text)
    for i in watson_text2.get("personality"):
        score = (i.get("name"), i.get("raw_score"))
        traits.append(score)

    traitPercentile = []

    # Converts personailty score to 100 percentile
    for trait in traits:
        traitPercentile.append((trait[0], "%.2f" % (trait[1]*100)))

    twitterCall.drop_table()
    twitterCall.close_db()

    return render_template('displayPersonality.html', listOfTweets=traitPercentile, user=tweets)
