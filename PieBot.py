from functions import *
import emoji
import schedule

pre_flight_checks()


# Buy more coins at a regular interval
def buy(pairs):
    total_portfolio_value = 0

    # Let users know the bot has been called and is running
    print()
    print(colored("Buy", "yellow"))
    print(emoji.emojize(":mag:", use_aliases=True), end=" ")
    print(colored("Checking if there is enough USDT available", "cyan"))

    total_portfolio_value = get_portfolio_value(pairs)
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


if environment == "production":
    print("Production")

else:
    buy(pairs=pair_list)
    # rebalance(pairs=pair_list)
