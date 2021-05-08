import hashlib
import hmac
import os
import sys
from termcolor import colored
import time

# Set environment variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ENVIRONMENT = os.getenv('ENVIRONMENT')


def buy_order(pair, quantity):
    print("Buy " + str(quantity) + " of " + pair)


def current_time():
    time_data = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    print(colored(time_data + ": ", "yellow"), end='')


def sign_request(req):
    param_string = ''

    if 'params' in req:
        for key in sorted(req['params']):
            param_string += key
            param_string += str(req['params'][key])

    sig_payload = req['method'] + str(req['id']) + req['api_key'] + param_string + str(req['nonce'])

    req['sig'] = hmac.new(
        bytes(str(API_SECRET), 'utf-8'),
        msg=bytes(sig_payload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return req
