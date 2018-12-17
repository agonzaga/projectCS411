from flask import Flask

app = Flask(__name__)
app.secret_key ="weirdo"

from mainApp import routes