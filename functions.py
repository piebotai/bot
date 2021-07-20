import hashlib
import hmac
import json
import requests
import sys
from termcolor import colored
import time

from _config import *


# Prints the current time
def current_time(new_line):
    time_data = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    if new_line:
        print(colored(time_data + ": ", "yellow"), end="")
    else:
        print(colored(time_data, "yellow"))


# Gets the total available value of the portfolio
def get_available_portfolio_value(value):
    # Keeps aside the defined USDT reserves
    usdt_reserve_value = (value / 100) * (usdt_reserve * 100)

    total_available_balance = value - usdt_reserve_value

    return total_available_balance


# Gets the total balance of a coin
def get_coin_balance(coin):
    coin_balance_request = {
        "id": 100,
        "method": "private/get-account-summary",
        "api_key": api_key,
        "params": {
            "currency": coin
        },
        "nonce": int(time.time() * 1000)
    }

    coin_balance_response = requests.post("https://api.crypto.com/v2/private/get-account-summary",
                                          headers={"Content-type": "application/json"},
                                          data=json.dumps(sign_request(req=coin_balance_request)))
    coin_balance_data = json.loads(coin_balance_response.content)
    coin_total_balance = coin_balance_data["result"]["accounts"][0]["available"]

    return coin_total_balance


# Gets the price of a coin pair
def get_coin_price(pair):
    get_price_response = requests.get("https://api.crypto.com/v2/public/get-ticker?instrument_name=" + pair)
    ticker = json.loads(get_price_response.content)
    coin_price = ticker["result"]["data"]["b"]

    return coin_price


# Gets the details of a coin pair
def get_pair_details(pair):
    def get_instrument(instruments, name):
        for instrument in instruments:
            if instrument["instrument_name"] == name:
                return instrument

    response = requests.get("https://api.crypto.com/v2/public/get-instruments")
    data = json.loads(response.content)
    instruments = data["result"]["instruments"]

    details = get_instrument(instruments, pair)

    return details


# Gets the total value of the portfolio
def get_portfolio_value(pairs, include_usdt):
    total_balance = 0

    for pair in pairs:
        # Gets the total number of coins for this coin pair
        coin_balance = get_coin_balance(pair[0])

        # Gets the current price for this coin pair
        coin_price = get_coin_price(pair[1])

        total_balance = total_balance + (coin_balance * coin_price)

    if include_usdt:
        # Get the total balance of USDT and add it to the current collected balance
        usdt_total_balance = get_coin_balance("USDT")

        total_balance = total_balance + usdt_total_balance

    return total_balance


# Submits a buy order
def order_buy(pair, notional):
    # Finds the required price precision for this coin pair
    pair_data = get_pair_details(pair)
    price_precision = pair_data["price_decimals"]

    # Converts the notional into a number with the correct number of decimal places
    notional = "%0.*f" % (price_precision, notional)

    order_buy_request = {
        "id": 100,
        "method": "private/create-order",
        "api_key": api_key,
        "params": {
            "instrument_name": pair,
            "side": "BUY",
            "type": "MARKET",
            "notional": notional
        },
        "nonce": int(time.time() * 1000)
    }

    order_buy_response = requests.post("https://api.crypto.com/v2/private/create-order",
                                  headers={"Content-type": "application/json"},
                                  data=json.dumps(sign_request(req=order_buy_request)))

    return order_buy_response


# Submits a sell order
def order_sell(pair, quantity):
    # Finds the required quantity precision for this coin pair
    pair_data = get_pair_details(pair)
    quantity_precision = pair_data["quantity_decimals"]

    # Converts the quantity into a number with the correct number of decimal places
    quantity = "%0.*f" % (quantity_precision, quantity)

    order_sell_request = {
        "id": 100,
        "method": "private/create-order",
        "api_key": api_key,
        "params": {
            "instrument_name": pair,
            "side": "SELL",
            "type": "MARKET",
            "quantity": quantity
        },
        "nonce": int(time.time() * 1000)
    }

    order_sell_response = requests.post("https://api.crypto.com/v2/private/create-order",
                                       headers={"Content-type": "application/json"},
                                       data=json.dumps(sign_request(req=order_sell_request)))

    return order_sell_response


# Checks everything is in order before the bot runs
def pre_flight_checks():
    print(colored("Performing pre-flight checks", "cyan"))

    # Checks whether the environment has been defined
    try:
        environment
    except NameError:
        print(colored("Your environment is missing from the config file", "red"))
        sys.exit()

    # Checks whether the API key and API secret have been defined
    try:
        api_key and api_secret
    except NameError:
        print(colored("Your API key and API secret are missing from the config file", "red"))
        sys.exit()

    # Checks whether the trading pairs have been defined, and if there is enough to begin trading
    try:
        pair_list
    except NameError:
        print(colored("Your trading coin pairs are missing from the config file", "red"))
        sys.exit()
    else:
        if len(pair_list) < 1:
            print(colored("You need to use at least one coin pair", "red"))
            sys.exit()

    # Checks whether the USDT reserves amount has been defined
    try:
        usdt_reserve
    except NameError:
        print(colored("Your USDT reserve amount is missing from the config file", "red"))
        sys.exit()
    else:
        if usdt_reserve < 0:
            print(colored("You need to define a valid USDT reserve. If you don't want to use a reserve, set the value as 0", "red"))
            sys.exit()
        elif usdt_reserve > 80:
            print(colored("Your USDT reserve must be 80% or lower", "red"))
            sys.exit()

    # Checks whether the minimum order value has been defined and is valid
    try:
        min_order_value
    except NameError:
        print(colored("Your minimum order value is missing from the config file", "red"))
        sys.exit()
    else:
        if min_order_value < 0.25:
            print(colored("Your minimum order value must be 0.25 or greater", "red"))
            sys.exit()

    # Checks whether the maximum Buy order value has been defined and is valid
    try:
        max_buy_order_value
    except NameError:
        print(colored("Your maximum Buy order value is missing from the config file", "red"))
        sys.exit()
    else:
        if max_buy_order_value < min_order_value:
            print(colored("Your maximum Buy order value cannot be smaller than your minimum order value", "red"))
            sys.exit()

    # Checks whether the maximum Rebalance order value has been defined and is valid
    try:
        max_rebalance_order_value
    except NameError:
        print(colored("Your maximum Rebalance order value is missing from the config file", "red"))
        sys.exit()
    else:
        if max_rebalance_order_value < min_order_value:
            print(colored("Your maximum Rebalance order value cannot be smaller than your minimum order value", "red"))
            sys.exit()

    # Send a private request to test if the API key and API secret are correct
    init_request = {
        "id": 100,
        "method": "private/get-account-summary",
        "api_key": api_key,
        "params": {
            "currency": "USDT"
        },
        "nonce": int(time.time() * 1000)
    }

    init_response = requests.post("https://api.crypto.com/v2/private/get-account-summary",
                                  headers={"Content-type": "application/json"},
                                  data=json.dumps(sign_request(req=init_request)))
    init_status = init_response.status_code

    if init_status == 200:
        # The bot can connect to the account, has been started, and is waiting to be called
        print(colored("Pre-flight checks successful", "green"))

    else:
        # Could not connect to the account
        print(colored("Could not connect to your account. Please ensure the API key and API secret are correct and have the right privileges", "red"))
        sys.exit()


# Signs private requests
def sign_request(req):
    param_string = ""

    if "params" in req:
        for key in sorted(req["params"]):
            param_string += key
            param_string += str(req["params"][key])

    sig_payload = req["method"] + str(req["id"]) + req["api_key"] + param_string + str(req["nonce"])

    req["sig"] = hmac.new(
        bytes(str(api_secret), "utf-8"),
        msg=bytes(sig_payload, "utf-8"),
        digestmod=hashlib.sha256
    ).hexdigest()

    return req
