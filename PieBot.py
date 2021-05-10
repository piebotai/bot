from functions import *
import emoji
import schedule

pre_flight_checks()


def piebot(pairs):
    # Let users know the bot has been called and is running
    print()
    current_time(False)
    print(emoji.emojize(':mag:', use_aliases=True), end=" ")
    print(colored("Collecting current balances", "cyan"))

    # Gets the USDT balance and keeps aside the defined reserves
    usdt_total_balance = get_coin_balance("USDT")

    if usdt_reserve > 0:
        usdt_balance = usdt_total_balance - usdt_reserve

    elif usdt_reserve == 0:
        usdt_balance = usdt_total_balance

    # Adds up the total balance of all enabled coins and the USDT balance
    total_balance = usdt_balance

    for pair in pairs:
        # Gets the total number of coins for this coin pair
        coin_balance = get_coin_balance(pair[0])

        # Gets the current price for this coin pair
        coin_price = get_coin_price(pair[1])

        total_balance = total_balance + (coin_balance * coin_price)

    # Equally divide the balance by the number of coins, so we know the target value each coin should aim for
    target_per_coin = total_balance / len(pair_list)

    print(emoji.emojize(':white_check_mark:', use_aliases=True), end=" ")
    print(colored("Balances collected", "green"))

    print(emoji.emojize(':money_bag:', use_aliases=True), end=" ")
    print(colored("Placing orders", "cyan"))

    for pair in pair_list:
        # Sets null defaults
        buy_order = False
        sell_order = False
        difference = 0
        order_value = 0
        pair_value = 0

        # Gets the total number of coins for this coin pair
        coin_balance = get_coin_balance(pair[0])

        # Gets the current price for this coin pair
        coin_price = get_coin_price(pair[1])

        pair_value = coin_balance * coin_price

        # If the coin pair value is over target, sell the excess if it's greater than the minimum order value
        if pair_value > target_per_coin:
            difference = pair_value - target_per_coin
            if difference >= min_order_value:
                sell_order = True
                order_value = difference / coin_price

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

        if buy_order:
            if ENVIRONMENT == "production":
                order_buy(pair[1], order_value)

            print_value = round(order_value, 2)
            current_time(True)
            print(str(print_value) + " USDT - " + pair[0], end=" ")
            print(colored("[BUY]", "green"))

        elif sell_order:
            if ENVIRONMENT == "production":
                order_sell(pair[1], order_value, pair[2])

            print_value = round(difference, 2)
            current_time(True)
            print(str(print_value) + " USDT - " + pair[0], end=" ")
            print(colored("[SELL]", "magenta"))

        else:
            current_time(True)
            print(pair[0], end=" ")
            print(colored("[SKIP]", "yellow"))

    print(emoji.emojize(':hourglass:', use_aliases=True), end=" ")
    print(colored("Waiting to be called", "cyan"))


if ENVIRONMENT == "production":
    print(emoji.emojize(':hourglass:', use_aliases=True), end=" ")
    print(colored("Waiting to be called", "cyan"))
    schedule.every().hour.at(":00").do(piebot, pairs=pair_list)

    while True:
        schedule.run_pending()
        time.sleep(1)

else:
    piebot(pairs=pair_list)
