import json

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from zoo import api

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['ERROR_404_HELP'] = False
api.init_app(app)