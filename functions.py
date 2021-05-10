import emoji
import hashlib
import hmac
import json
import os
import requests
import sys
from termcolor import colored
import time

from _config import *

# Set environment variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
ENVIRONMENT = os.getenv('ENVIRONMENT')


# Prints the current time
def current_time(new_line):
    time_data = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    if new_line:
        print(colored(time_data + ": ", "yellow"), end="")
    else:
        print(colored(time_data, "yellow"))


# Gets the total balance of a coin
def get_coin_balance(coin):
    coin_balance_request = {
        "id": 100,
        "method": "private/get-account-summary",
        "api_key": API_KEY,
        "params": {
            "currency": coin
        },
        "nonce": int(time.time() * 1000)
    }

    coin_balance_response = requests.post('https://api.crypto.com/v2/private/get-account-summary',
                                          headers={'Content-type': 'application/json'},
                                          data=json.dumps(sign_request(req=coin_balance_request)))
    coin_balance_data = json.loads(coin_balance_response.content)
    coin_total_balance = coin_balance_data['result']['accounts'][0]['balance']

    return coin_total_balance


# Gets the price of a coin pair
def get_coin_price(pair):
    get_price_response = requests.get("https://api.crypto.com/v2/public/get-ticker?instrument_name=" + pair)
    ticker = json.loads(get_price_response.content)
    coin_price = ticker['result']['data']['b']

    return coin_price


def order_buy(pair, notional):
    order_buy_request = {
        "id": 100,
        "method": "private/create-order",
        "api_key": API_KEY,
        "params": {
            "instrument_name": pair,
            "side": "BUY",
            "type": "MARKET",
            "notional": notional
        },
        "nonce": int(time.time() * 1000)
    }

    order_buy_response = requests.post('https://api.crypto.com/v2/private/create-order',
                                  headers={'Content-type': 'application/json'},
                                  data=json.dumps(sign_request(req=order_buy_request)))


def order_sell(pair, quantity):
    order_sell_request = {
        "id": 100,
        "method": "private/create-order",
        "api_key": API_KEY,
        "params": {
            "instrument_name": pair,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity
        },
        "nonce": int(time.time() * 1000)
    }

    order_sell_response = requests.post('https://api.crypto.com/v2/private/create-order',
                                       headers={'Content-type': 'application/json'},
                                       data=json.dumps(sign_request(req=order_sell_request)))


def pre_flight_checks():
    print(emoji.emojize(':rocket:', use_aliases=True), end=" ")
    print(colored("Performing pre-flight checks", "cyan"))

    time.sleep(1)

    # Kill the script if the API key and API secret aren't defined
    if not API_KEY and API_SECRET:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored(".env is missing your API key and secret", "red"))
        sys.exit()

    # Kill the script if no environment has been defined
    if not ENVIRONMENT:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored(".env is missing a defined environment. This should either be 'production' or 'dev'", "red"))
        sys.exit()

    # Checks whether the trading pairs have been defined, and if there is enough to begin trading
    try:
        pair_list
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your trading coin pairs are missing from the config file", "red"))
        sys.exit()
    else:
        if len(pair_list) < 1:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("You need to use at least one coin pair", "red"))
            sys.exit()

    # Checks whether the USDT reserves amount has been defined
    try:
        usdt_reserve
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your USDT reserve amount is missing from the config file", "red"))
        sys.exit()
    else:
        if usdt_reserve < 0:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("You need to define a valid USDT reserve. If you don't want to use a reserve, set the value as 0", "red"))
            sys.exit()
        elif usdt_reserve > 80:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("Your USDT reserve must be 80% or lower", "red"))
            sys.exit()

    # Send a private request to test if the API key and API secret are correct
    init_request = {
        "id": 100,
        "method": "private/get-account-summary",
        "api_key": API_KEY,
        "params": {
            "currency": "USDT"
        },
        "nonce": int(time.time() * 1000)
    }

    init_response = requests.post('https://api.crypto.com/v2/private/get-account-summary',
                                  headers={'Content-type': 'application/json'},
                                  data=json.dumps(sign_request(req=init_request)))
    init_status = init_response.status_code

    if init_status == 200:
        # The bot can connect to the account, has been started, and is waiting to be called
        print(emoji.emojize(':white_check_mark:', use_aliases=True), end=" ")
        print(colored("Pre-flight checks successful", "green"))

    else:
        # Could not connect to the account
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Could not connect to your account. Please ensure the API key and API secret are correct and have the right privileges", "red"))
        sys.exit()


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
