# -*- coding: utf-8 -*-

# Import required packages
import asyncio
import aioschedule as schedule
import cryptocom.exchange as cro
import os
from termcolor import colored
import time

# Set environment variables
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Let users know the bot has started, and is waiting to be called
print(colored("Bot started", "green"))


async def rebalance():
    # Lets users know the bot has been called and is running
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S - %d/%m/%Y", t)
    print(colored(current_time + ": ", "yellow"), end='')
    print(colored("Running...", "cyan"))

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

    # Adds up the total balance of all enabled coins and the USDT balance
    total_balance = usdt_balance
    for pair in pairs:
        total_coins = balances[cro.coins.Coin(pair[0])].total
        coin_price = await exchange.get_price(cro.pairs.Pair(pair[1], 9, 9))
        total_balance = total_balance + (total_coins * coin_price)

    # Equally divide the balance by the number of coins, so we know the target value each coin should aim for
    target_per_coin = total_balance / len(pairs)

    # Sets the minimum and maximum order values, so we don't eat into our USDT balance too quickly
    min_order_value = 0.25
    max_order_value = 0.40

    for pair in pairs:
        # Sets null defaults
        buy_order = False
        sell_order = False
        difference = 0
        order_value = 0

        # Calculate the USDT value of this coin pair
        pair_total_coins = balances[cro.coins.Coin(pair[0])].total
        pair_coin_price = await exchange.get_price(cro.pairs.Pair(pair[1], 9, 9))
        pair_value = pair_total_coins * pair_coin_price

        # If the coin pair value is over target, sell the excess if it's greater than the minimum order value
        if pair_value > target_per_coin:
            difference = pair_value - target_per_coin
            if difference >= min_order_value:
                sell_order = True
                order_value = difference / await exchange.get_price(cro.pairs.Pair(pair[1], 9, 9))

        # If the coin pair value is under target, work out how much we need to buy
        elif pair_value < target_per_coin:
            difference = target_per_coin - pair_value

            # If the difference is between min_order_value and max_order_value (inclusive), set the difference as the order value
            if min_order_value <= difference <= max_order_value:
                buy_order = True
                order_value = difference

            # If the difference is greater than max_order_value, set the order value as max_order_value
            elif difference > max_order_value:
                buy_order = True
                order_value = max_order_value

        # Submit a buy order if necessary
        if buy_order:
            await account.buy_market(cro.pairs.Pair(pair[1], pair[2], pair[3]), order_value)
            print_value = round(order_value, 2)
            print(colored(current_time + ": ", "yellow"), end='')
            print(str(print_value) + " USDT - " + pair[0], end='')
            print(colored(" [BUY]", "green"))

        # Submit a sell order if necessary
        elif sell_order:
            await account.sell_market(cro.pairs.Pair(pair[1], pair[2], pair[3]), order_value)
            print_value = round(difference, 2)
            print(colored(current_time + ": ", "yellow"), end='')
            print(str(print_value) + " USDT - " + pair[0], end='')
            print(colored(" [SELL]", "magenta"))

        # Neither a buy or sell order was required this time, so print a user friendly message
        else:
            print(colored(current_time + ": ", "yellow"), end='')
            print(pair[0], end='')
            print(colored(" [SKIP]", "yellow"))

    print(colored("Waiting...", "cyan"))

schedule.every().hour.at(":00").do(rebalance)

loop = asyncio.get_event_loop()

while True:
    loop.run_until_complete(schedule.run_pending())
    time.sleep(1)
