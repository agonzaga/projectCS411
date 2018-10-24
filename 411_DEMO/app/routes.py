from flask import render_template, request
from app import app, apiCall
import requests
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/enter', methods=['POST'])
def index2():
    currency = request.form["twitter"]
    ret = apiCall.func(currency)
    y = json.loads(ret)
    return str(y["CAD_USD"]["val"])
