# -*- coding: utf-8 -*-

#
# Stake Progress
# This script returns a visual indicator of how many more coins are required for each pair
# to meet the minimum staking requirements on the Crypto.com App,
# as well as the USDT value of those coins
#

# Import required packages
import os
import asyncio
import cryptocom.exchange as cro
from termcolor import colored

# Set environment variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')


async def stake_progress():
    exchange = cro.Exchange()
    account = cro.Account(api_key=API_KEY, api_secret=API_SECRET)
    await account.sync_pairs()
    balances = await account.get_balance()

    pairs = [
        ("ADA", "ADA_USDT", 5, 1, 250),
        ("ALGO", "ALGO_USDT", 4, 2, 150),
        ("ATOM", "ATOM_USDT", 3, 2, 12),
        ("BTC", "BTC_USDT", 2, 6, 0.005),
        ("CRO", "CRO_USDT", 5, 3, 5000),
        ("DOT", "DOT_USDT", 4, 3, 10),
        ("ETH", "ETH_USDT", 2, 5, 0.15),
        ("LTC", "LTC_USDT", 2, 5, 1.5),
        ("XLM", "XLM_USDT", 5, 1, 450),
        ("XRP", "XRP_USDT", 5, 1, 450)
    ]

    # Let users know the bot has been called and is running
    print(colored("Getting current balance for all enabled coin pairs", "green"))

    for pair in pairs:
        total_coins = balances[cro.coins.Coin(pair[0])].total
        minimum_stake = pair[4]

        print()

        print(colored(pair[0], "cyan"))

        print(colored("Minimum stake:", "yellow"), end=" ")
        print(str(minimum_stake) + " " + pair[0])

        print(colored("Current balance:", "yellow"), end=" ")
        print(str(total_coins) + " " + pair[0], end=" ")

        pair_difference = minimum_stake - total_coins

        if pair_difference == 0:
            print(colored("[ON TARGET]", "yellow"))

        elif pair_difference > 0:
            print(colored("[UNDER TARGET]", "red"))
            print(colored("Coins remaining:", "yellow"), end=" ")
            print(str(pair_difference) + " " + pair[0], end=" ")
            coin_price = await exchange.get_price(cro.pairs.Pair(pair[1], 9, 9))
            print(colored("(" + str(round(coin_price * pair_difference, 2)) + " USDT)", "magenta"))

        elif pair_difference < 0:
            print(colored("[OVER TARGET]", "green"))

        print()

asyncio.run(stake_progress())
