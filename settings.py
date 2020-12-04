import json
from flask import Flask

CONFIG = {}

with open('config.json') as json_file:
    CONFIG = json.load(json_file)

API_KEY = CONFIG['API_KEY']
TIMEOUT = CONFIG.get('TIMEOUT', 5)
TRX_ACCOUNT_BALANCE_URI = "https://api.trongrid.io/v1/accounts/"

APP = Flask(__name__)
