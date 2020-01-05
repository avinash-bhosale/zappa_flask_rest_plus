import json

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from zoo import api

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config['ERROR_404_HELP'] = False
api.init_app(app)

"""
@app.after_request
def after_request(response):
    data = response.get_json()
    if type(data) is dict:
        print("it's dict")
        '''
        if 'statusCode' not in data:
            data['statusCodes'] = 200
        '''
        print(data)
        response.data = json.dumps(data)

    return response
"""

app.run(debug=True)
