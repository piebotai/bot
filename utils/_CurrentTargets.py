# -*- coding: utf-8 -*-

#
# Current Targets
# This script returns a visual indicator of the current target values for each coin,
# in accordance with the logic outlined in PieBot.py
#

# Import required packages
import os
import asyncio
import cryptocom.exchange as cro
from termcolor import colored
import time

# Set environment variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')


async def current_targets():
    exchange = cro.Exchange()
    account = cro.Account(api_key=API_KEY, api_secret=API_SECRET)
    await account.sync_pairs()
    balances = await account.get_balance()

    pairs = [
        ("ADA", "ADA_USDT", 5, 1),
        ("ALGO", "ALGO_USDT", 4, 2),
        ("ATOM", "ATOM_USDT", 3, 2),
        ("BTC", "BTC_USDT", 2, 6),
        ("CRO", "CRO_USDT", 5, 3),
        ("DOT", "DOT_USDT", 4, 3),
        ("ETH", "ETH_USDT", 2, 5),
        ("LTC", "LTC_USDT", 2, 5),
        ("XLM", "XLM_USDT", 5, 1),
        ("XRP", "XRP_USDT", 5, 1)
    ]

    # Gets the USDT balance and keeps 25 USDT aside
    usdt_balance = balances[cro.coins.USDT].total - 25

    # Let users know the bot has been called and is running
    print(colored("Getting current prices for all enabled coin pairs", "green"))

    # Adds up the total balance of all enabled coins and the USDT balance
    total_balance = usdt_balance
    for pair in pairs:
        time.sleep(0.1)
        total_coins = balances[cro.coins.Coin(pair[0])].total
        coin_price = await exchange.get_price(cro.pairs.Pair(pair[1], 9, 9))
        total_balance = total_balance + (total_coins * coin_price)

    # Equally divide the balance by the number of coins, so we know the target value each coin should aim for
    target_per_coin = round(total_balance / len(pairs), 2)

    # Show users the current target USDT value per coin pair
    print(colored("Target per coin:", "cyan"), end=' ')
    print(target_per_coin, end=' ')
    print("USDT")

    print()

    for pair in pairs:
        time.sleep(0.1)

        # Calculate the USDT value of this coin pair
        pair_total_coins = balances[cro.coins.Coin(pair[0])].total
        pair_coin_price = await exchange.get_price(cro.pairs.Pair(pair[1], 9, 9))
        pair_value = round(pair_total_coins * pair_coin_price, 2)

        pair_difference = round((pair_value - target_per_coin), 2)

        print(colored(pair[0] + ":", "cyan"), end=' ')
        print(pair_value, end=' ')
        print("(" + str(pair_difference) + " USDT)", end=' ')

        if pair_difference == 0:
            print(colored("[ON TARGET]", "yellow"))
        elif pair_difference < 0:
            print(colored("[UNDER TARGET]", "red"))
        elif pair_difference > 0:
            print(colored("[OVER TARGET]", "green"))

asyncio.run(current_targets())
