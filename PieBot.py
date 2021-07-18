from functions import *
import emoji
import schedule

pre_flight_checks()


# Buy more coins at a regular interval
def buy(pairs):
    # Let users know the bot has been called and is running
    print()
    print(colored("Buy", "yellow"))
    print(emoji.emojize(":mag:", use_aliases=True), end=" ")
    print(colored("Checking if there is enough USDT available", "cyan"))

    total_portfolio_value = get_portfolio_value(pairs, True)
    total_usdt_reserve = (total_portfolio_value / 100) * (usdt_reserve * 100)

    total_usdt_value = get_coin_balance("USDT")
    total_usdt_available = total_usdt_value - total_usdt_reserve
    required_usdt = max_order_value * len(pairs)

    if required_usdt <= total_usdt_available:
        print(emoji.emojize(":money_bag:", use_aliases=True), end=" ")
        print(colored("Placing orders", "cyan"))

        for pair in pairs:
            order_value = max_order_value

            if environment == "production":
                order_confirmed = False
                order = order_buy(pair[1], order_value)
                time.sleep(0.1)
                if order.status_code == 200:
                    order_confirmed = True

                print_value = round(order_value, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[BUY]", "green"), end=" ")

                if order_confirmed:
                    print(emoji.emojize(":white_check_mark:", use_aliases=True))
                else:
                    print(emoji.emojize(":x:", use_aliases=True))
                    print(order.status_code, order.reason)
                    print(order.content)

            else:
                print_value = round(order_value, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[BUY]", "green"))

    else:
        print(emoji.emojize(":money_with_wings:", use_aliases=True), end=" ")
        print(colored("Not enough USDT available", "yellow"))


# Rebalance all coin pairs so they are on target
def rebalance(pairs):
    # Let users know the bot has been called and is running
    print()
    print(colored("Rebalance", "yellow"))
    print(emoji.emojize(":mag:", use_aliases=True), end=" ")
    print(colored("Collecting current balances", "cyan"))

    total_portfolio_value = get_portfolio_value(pairs, False)

    # Equally divide the balance by the number of coins, so we know the target value each coin should aim for
    target_per_coin = total_portfolio_value / len(pairs)

    print(emoji.emojize(":white_check_mark:", use_aliases=True), end=" ")
    print(colored("Balances collected", "green"))

    print(emoji.emojize(":money_bag:", use_aliases=True), end=" ")
    print(colored("Placing orders", "cyan"))

    for pair in pairs:
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
            if environment == "production":
                order_confirmed = False
                order = order_buy(pair[1], order_value)
                time.sleep(0.25)
                if order.status_code == 200:
                    order_confirmed = True

                print_value = round(order_value, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[BUY]", "green"), end=" ")

                if order_confirmed:
                    print(emoji.emojize(":white_check_mark:", use_aliases=True))
                else:
                    print(emoji.emojize(":x:", use_aliases=True))
                    print(order.status_code, order.reason)
                    print(order.content)

            else:
                print_value = round(order_value, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[BUY]", "green"))

        elif sell_order:
            if environment == "production":
                order_confirmed = False
                order = order_sell(pair[1], order_value)
                time.sleep(0.25)
                if order.status_code == 200:
                    order_confirmed = True

                print_value = round(difference, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[SELL]", "magenta"), end=" ")

                if order_confirmed:
                    print(emoji.emojize(":white_check_mark:", use_aliases=True))
                else:
                    print(emoji.emojize(":x:", use_aliases=True))
                    print(order.status_code, order.reason)
                    print(order.content)

            else:
                print_value = round(difference, 2)
                current_time(True)
                print(str(print_value) + " USDT - " + pair[0], end=" ")
                print(colored("[SELL]", "magenta"))

        else:
            current_time(True)
            print(pair[0], end=" ")
            print(colored("[SKIP]", "yellow"))

    print(emoji.emojize(":hourglass:", use_aliases=True), end=" ")
    print(colored("Waiting to be called", "cyan"))


if environment == "production":
    print("Production")

else:
    rebalance(pairs=pair_list)
    # rebalance(pairs=pair_list)
