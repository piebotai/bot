import hashlib
import hmac
import json
import requests
from termcolor import colored
import time

environment = "dev"
api_key = "xxx"
api_secret = "xxx"

# The list of coin pairs you want to trade with
pair_list = [
    ("ADA", "ADA_USDT", 250, 105.7),
    ("ALGO", "ALGO_USDT", 150, 150.5621),
    ("ATOM", "ATOM_USDT", 12, 11.2777),
    ("BTC", "BTC_USDT", 0.005, 0.0036171),
    ("CRO", "CRO_USDT", 5000, 1443.94),
    ("DOGE", "DOGE_USDT", 500, 0),
    ("DOT", "DOT_USDT", 10, 6.5683999985),
    ("ETH", "ETH_USDT", 0.15, 0.579628),
    ("LTC", "LTC_USDT", 1.5, 0.93121405),
    ("VET", "VET_USDT", 5000, 0),
    ("XLM", "XLM_USDT", 450, 1240.7868571),
    ("XRP", "XRP_USDT", 450, 663.13096)
]


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


# Signs private requests
def sign_request(req):
    param_string = ''

    if 'params' in req:
        for key in sorted(req['params']):
            param_string += key
            param_string += str(req['params'][key])

    sig_payload = req['method'] + str(req['id']) + req['api_key'] + param_string + str(req['nonce'])

    req['sig'] = hmac.new(
        bytes(str(api_secret), 'utf-8'),
        msg=bytes(sig_payload, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return req


total_remaining_value = 0

for pair in pair_list:
    print(colored(pair[0], "cyan"))

    print(colored("Target:", "yellow"), end=" ")
    print(str(pair[2]) + " " + pair[0])

    currentBalance = get_coin_balance(pair[0])
    existingBalance = pair[3]
    balance = currentBalance + existingBalance
    print(colored("Current balance:", "yellow"), end=" ")
    print(str(balance) + " " + pair[0])

    difference = ((pair[2] - balance) * -1)
    print(colored("Coins remaining:", "yellow"), end=" ")
    if difference > 0:
        print("Over target", end=" ")
    else:
        print(str(difference * -1) + " " + pair[0], end=" ")

    coin_price = get_coin_price(pair[1])
    difference_value = difference * coin_price
    if difference > 0:
        print(colored("(" + str(round(difference_value, 2)) + " USDT)", "green"))
    else:
        print(colored("(" + str(round(difference_value, 2)) + " USDT)", "red"))

    if difference < 0:
        total_remaining_value = total_remaining_value + difference_value

    print()

print("Total remaining value:", end=" ")

if total_remaining_value > 0:
    print(colored(str(round(total_remaining_value, 2)) + " USDT", "green"))
else:
    print(colored(str(round(total_remaining_value * -1, 2)) + " USDT", "red"))
