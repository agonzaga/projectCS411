from flask import render_template, request
from mainApp import app, twitterCall
import requests
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/getTweets', methods=['POST'])
def index2():
    tweets = request.form["twitter"]
    ret = twitterCall.get_tweets(tweets)
    # res = json.loads(ret)
    return render_template('displayTweets.html', listOfTweets=ret)
