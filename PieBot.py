from functions import *
import argparse
import gc
import schedule
import signal

pre_flight_checks()


# Hard codes the minimum order value
min_order_value = 0.25

# Checks whether the Rebalance threshold has been defined, and allows the bot to run if it hasn't
try:
    rebalance_threshold
except NameError:
    rebalance_threshold = None

if rebalance_threshold is None:
    uses_threshold = False
else:
    if rebalance_threshold > 0:
        uses_threshold = True
    else:
        uses_threshold = False


# Buy more coins at a regular interval
def buy(pairs):
    # Let users know the bot has been called and is running
    print()
    print(colored("Buy", "yellow"))
    print(colored("Placing orders...", "cyan"))

    total_portfolio_value = get_portfolio_value(pairs, True)
    total_usdt_reserve = (total_portfolio_value / 100) * (usdt_reserve * 100)

    total_usdt_value = get_coin_balance("USDT")
    total_usdt_available = total_usdt_value - total_usdt_reserve
    required_usdt = buy_order_value * len(pairs)

    if required_usdt <= total_usdt_available:
        for pair in pairs:
            order_value = buy_order_value

            if environment == "production":
                order_confirmed = False
                order = order_buy(pair[1], order_value)
                time.sleep(0.1)
                if order.status_code == 200:
                    order_confirmed = True

                print_value = round(order_value, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[BUY]", "green"))

                if not order_confirmed:
                    print(order.status_code, order.reason)
                    print(order.content)

            else:
                print_value = round(order_value, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[BUY]", "green"))

    else:
        print(colored("Not enough USDT available", "yellow"))

    gc.collect()

    print(colored("Waiting to be called...", "cyan"))


# Rebalance all coins so they are on target
def rebalance(pairs):
    # Let users know the bot has been called and is running
    print()
    print(colored("Rebalance", "yellow"))
    print(colored("Placing orders...", "cyan"))

    order_data = []
    total_portfolio_value = 0

    for pair in pairs:
        coin_balance = get_coin_balance(pair[0])
        coin_price = get_coin_price(pair[1])
        pair_value = coin_balance * coin_price

        order_data.append([pair[0], pair[1], coin_price, pair_value])
        total_portfolio_value += pair_value

    # Equally divide the balance by the number of coins, so we know the target value each coin should aim for
    target_per_coin = total_portfolio_value / len(pairs)

    buy_orders_data = []
    sell_orders_data = []

    for pair in order_data:
        coin_price = pair[2]
        pair_value = pair[3]

        # The coin value is over target
        if pair_value > target_per_coin:
            difference = pair_value - target_per_coin

            if uses_threshold:
                print("Threshold")

            else:
                if difference >= min_order_value:
                    order_value = difference / coin_price
                    sell_orders_data.append([pair[0], pair[1], order_value, difference])

        # The coin value is under target
        elif pair_value < target_per_coin:
            difference = target_per_coin - pair_value

            if uses_threshold:
                print("Threshold")

            else:
                if difference >= min_order_value:
                    order_value = difference
                    buy_orders_data.append([pair[0], pair[1], order_value, difference])

    if len(sell_orders_data) >= 1:
        for order in sell_orders_data:
            if environment == "production":
                order_confirmed = False
                order_request = order_sell(order[1], order[2])
                time.sleep(0.1)
                if order_request.status_code == 200:
                    order_confirmed = True

                print_value = round(order[3], 2)
                current_time(True)
                print(str(print_value) + " USDT - " + order[0], end=" ")
                print(colored("[SELL]", "magenta"))

                if not order_confirmed:
                    print(order_request.status_code, order_request.reason)
                    print(order_request.content)

            else:
                print_value = round(order[3], 2)
                current_time(True)
                print(str(print_value) + " USDT - " + order[0], end=" ")
                print(colored("[SELL]", "magenta"))

    if len(buy_orders_data) >= 1:
        for order in buy_orders_data:
            if environment == "production":
                order_confirmed = False
                order_request = order_buy(order[1], order[2])
                time.sleep(0.1)
                if order_request.status_code == 200:
                    order_confirmed = True

                print_value = round(order[3], 2)
                current_time(True)
                print(str(print_value) + " USDT - " + order[0], end=" ")
                print(colored("[BUY]", "green"))

                if not order_confirmed:
                    print(order_request.status_code, order_request.reason)
                    print(order_request.content)

            else:
                print_value = round(order[3], 2)
                current_time(True)
                print(str(print_value) + " USDT - " + order[0], end=" ")
                print(colored("[BUY]", "green"))

    total_orders = len(sell_orders_data) + len(buy_orders_data)
    if total_orders == 0:
        current_time(True)
        print(colored("No coins were eligible to be rebalanced", "yellow"))

    del order_data
    del buy_orders_data
    del sell_orders_data
    gc.collect()

    print(colored("Waiting to be called...", "cyan"))


if environment == "production":
    print(colored("Waiting to be called...", "cyan"))

    if rebalance_frequency > 0:
        schedule.every(rebalance_frequency).hours.at(":00").do(rebalance, pairs=pair_list)

    schedule.every(buy_frequency).hours.at(":30").do(buy, pairs=pair_list)

    stop = StopSignal()

    while not stop.stop_now:
        schedule.run_pending()
        time.sleep(1)

else:
    parser = argparse.ArgumentParser()
    parser.add_argument("task")
    args = parser.parse_args()
    if (args.task == "buy") or (args.task == "Buy"):
        buy(pairs=pair_list)

    elif (args.task == "rebalance") or (args.task == "Rebalance"):
        rebalance(pairs=pair_list)

    else:
        print(colored("Please specify which task you want to run", "red"))
