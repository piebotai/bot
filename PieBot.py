import hashlib
import hmac
import json
import os
import requests
import schedule
import sys
from termcolor import colored
import time

# Set environment variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ENVIRONMENT = os.getenv('ENVIRONMENT')

# Kill the script if no environment has been defined
if not ENVIRONMENT:
    print(colored(".env is missing a defined environment. This should either be 'production' or 'dev'", "red"))
    sys.exit()

pair_list = [
    "ADA_USDT",
    "ALGO_USDT",
    "ATOM_USDT",
    "BTC_USDT",
    "CRO_USDT",
    "DOT_USDT",
    "ETH_USDT",
    "LTC_USDT",
    "XLM_USDT",
    "XRP_USDT"
]

# Let users know the bot has started, and is waiting to be called
print(colored("Bot started", "green"))


def sign_request(req):
    # Ensure the params are alphabetically sorted by key
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


def piebot(pairs):
    if len(pairs) < 1:
        print(colored("You need to use at least one coin pair", "red"))
        sys.exit()

    # Let users know the bot has been called and is running
    current_time = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    print(colored(current_time + ": ", "yellow"), end='')
    print(colored("Collecting current balances", "cyan"))

    # Gets the USDT balance and keeps 25 USDT aside
    usdt_total_balance = 0
    usdt_balance = 0
    usdt_balance_request = {
        "id": 100,
        "method": "private/get-account-summary",
        "api_key": API_KEY,
        "params": {
            "currency": "USDT"
        },
        "nonce": int(time.time() * 1000)
    }

    # Sign the post request payload.
    usdt_balance_request = sign_request(req=usdt_balance_request)

    # Request the users account summary.
    headers = {'Content-type': 'application/json'}
    usdt_balance_response = requests.post('https://api.crypto.com/v2/private/get-account-summary', headers=headers, data=json.dumps(usdt_balance_request))
    usdt_balance_summary = json.loads(usdt_balance_response.content)
    usdt_total_balance = usdt_balance_summary['result']['accounts'][0]['balance']
    print(usdt_total_balance)

    if usdt_total_balance > 0:
        usdt_balance = usdt_total_balance - 25
        print(usdt_balance)
    else:
        print(colored("Could not get the current USDT balance for your account", "red"))
        sys.exit()

    current_time = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    print(colored(current_time + ": ", "yellow"), end='')
    print(colored("Portfolio balances collected", "green"))

    time.sleep(2)

    current_time = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    print(colored(current_time + ": ", "yellow"), end='')
    print(colored("Placing orders", "green"))


if ENVIRONMENT == "production":
    schedule.every().hour.at(":00").do(piebot, pairs=pair_list)

    while True:
        schedule.run_pending()
        time.sleep(1)

else:
    piebot(pairs=pair_list)
