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

# Kill the script if the API key and API secret aren't defined
if not API_KEY and API_SECRET:
    print(colored(".env is missing your API key and secret", "red"))
    sys.exit()

# Kill the script if no environment has been defined
if not ENVIRONMENT:
    print(colored(".env is missing a defined environment. This should either be 'production' or 'dev'", "red"))
    sys.exit()

pair_list = [
    ("ADA", "ADA_USDT"),
    ("ALGO", "ALGO_USDT"),
    ("ATOM", "ATOM_USDT"),
    ("BTC", "BTC_USDT"),
    ("CRO", "CRO_USDT"),
    ("DOT", "DOT_USDT"),
    ("ETH", "ETH_USDT"),
    ("LTC", "LTC_USDT"),
    ("XLM", "XLM_USDT"),
    ("XRP", "XRP_USDT")
]


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
    print(colored("Bot started", "green"))
else:
    # Could not connect to the account
    print(colored("Could not connect to your account. Please ensure the API key and API secret are correct", "red"))
    sys.exit()


def current_time():
    time_data = time.strftime("%H:%M:%S - %d/%m/%Y", time.localtime())
    print(colored(time_data + ": ", "yellow"), end='')


def piebot(pairs):
    if len(pairs) < 1:
        print(colored("You need to use at least one coin pair", "red"))
        sys.exit()

    # Let users know the bot has been called and is running
    current_time()
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

    usdt_balance_response = requests.post('https://api.crypto.com/v2/private/get-account-summary',
                                          headers={'Content-type': 'application/json'},
                                          data=json.dumps(sign_request(req=usdt_balance_request)))
    usdt_balance_data = json.loads(usdt_balance_response.content)
    usdt_total_balance = usdt_balance_data['result']['accounts'][0]['balance']
    print(usdt_total_balance)

    if usdt_total_balance > 0:
        usdt_balance = usdt_total_balance - 25
        print(usdt_balance)
    else:
        print(colored("Could not get the current USDT balance for your account", "red"))
        sys.exit()

    # Adds up the total balance of all enabled coins and the USDT balance
    total_balance = usdt_balance
    for pair in pairs:
        # Gets the total number of coins for this coin pair
        coin_balance = 0
        coin_balance_request = {
            "id": 100,
            "method": "private/get-account-summary",
            "api_key": API_KEY,
            "params": {
                "currency": pair[0]
            },
            "nonce": int(time.time() * 1000)
        }

        coin_balance_request = sign_request(req=coin_balance_request)
        coin_balance_response = requests.post('https://api.crypto.com/v2/private/get-account-summary',
                                              headers={'Content-type': 'application/json'},
                                              data=json.dumps(coin_balance_request))
        coin_balance_data = json.loads(coin_balance_response.content)
        coin_balance = coin_balance_data['result']['accounts'][0]['balance']

        get_price_response = requests.get("https://api.crypto.com/v2/public/get-ticker?instrument_name=" + pair[1])
        ticker = json.loads(get_price_response.content)
        coin_price = ticker['result']['data']['b']

        total_balance = total_balance + (coin_balance * coin_price)
        print(total_balance)

    current_time()
    print(colored("Portfolio balances collected. Calculating targets", "green"))

    time.sleep(0.5)

    # Equally divide the balance by the number of coins, so we know the target value each coin should aim for
    target_per_coin = total_balance / len(pair_list)
    if target_per_coin > 0:
        current_time()
        print("Target per coin: " + str(target_per_coin) + " USDT")
    else:
        print(colored("Could not calculate a suitable target for each coin pair", "red"))
        sys.exit()


if ENVIRONMENT == "production":
    schedule.every().hour.at(":00").do(piebot, pairs=pair_list)

    while True:
        schedule.run_pending()
        time.sleep(1)

else:
    piebot(pairs=pair_list)
