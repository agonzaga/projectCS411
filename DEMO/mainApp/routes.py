from flask import render_template, request
from mainApp import app, twitterCall
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


@app.route('/getTweets', methods=['POST'])
def displayTweets():
    tweets = request.form["twitter"]
    ret = twitterCall.get_tweets(tweets)
    if(ret == 0):
        return render_template('getTweet.html', status=True, msg='The given username does not exist.')
    # res = json.loads(ret)

    d = {"contentItems": []}
    for item in ret:
    	d["contentItems"].append({"content":item})


    return render_template('displayTweets.html', listOfTweets=ret)
