from flask import render_template, request, session, redirect
from mainApp import app, twitterCall, watsonCall, Login
import requests
import json
import sqlite3


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/getTweet')
def getTweetHtml():
    return render_template('getTweet.html')


@app.route('/login')
def login():
    return Login.login_twitter()


@app.route('/oauth-authorized')
def oauth_authorized():
    return Login.login_twitter().oauth()

@app.route('/getTweets', methods=['POST'])
def displayTweets():
    tweets = request.form["twitter"]
    ret = twitterCall.get_tweets(tweets)
    if(ret == 0):
        return render_template('getTweet.html', status=True, msg='The given username does not exist.')
    # res = json.loads(ret)

    d = {"contentItems": []}
    for item in ret:
        if ("https://" in item or "http://" in item):
            item = item[:item.find("http")]
        d["contentItems"].append({"content": item})

    with open("profile.json", "w") as file:
        file.write(json.dumps(d))

    traits = []
    watson_text = watsonCall.watson("../profile.json")
    watson_text2 = json.loads(watson_text)
    for i in watson_text2.get("personality"):
        score = (i.get("name"), i.get("raw_score"))
        traits.append(score)

    print(traits)
    return render_template('displayTweets.html', listOfTweets=traits)
