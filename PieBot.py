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

# Let users know the bot has started, and is waiting to be called
print(colored("Bot started", "green"))

async def PieBot():
    print("Works")


if ENVIRONMENT == "production":
    schedule.every().hour.at(":00").do(PieBot)

    loop = asyncio.get_event_loop()

    while True:
        loop.run_until_complete(schedule.run_pending())
        time.sleep(1)

else:
    asyncio.run(PieBot())
