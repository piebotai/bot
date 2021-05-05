import asyncio
import aioschedule as schedule
import hashlib
import hmac
import json
import os
import requests
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


async def piebot(pairs):
    if len(pairs) < 1:
        print(colored("You need to use at least one coin pair", "red"))
        sys.exit()

    # Let users know the bot has been called and is running
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S - %d/%m/%Y", t)
    print(colored(current_time + ": ", "yellow"), end='')
    print(colored("Running...", "cyan"))


if ENVIRONMENT == "production":
    schedule.every().hour.at(":00").do(piebot)

    loop = asyncio.get_event_loop()

    while True:
        loop.run_until_complete(schedule.run_pending())
        time.sleep(1)

else:
    asyncio.run(piebot(pairs=pair_list))
