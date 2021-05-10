from functions import *
import emoji
import schedule

pre_flight_checks()


def piebot(pairs):
    # Let users know the bot has been called and is running
    current_time()
    print(emoji.emojize(':mag:', use_aliases=True), end=" ")
    print(colored("Collecting current balances", "cyan"))

    # Gets the USDT balance and keeps aside the defined reserves
    usdt_total_balance = get_coin_balance("USDT")

    if usdt_reserve > 0:
        usdt_balance = usdt_total_balance - (usdt_total_balance * (usdt_reserve / 100))

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

    current_time()
    print(emoji.emojize(':white_check_mark:', use_aliases=True), end=" ")
    print(colored("Balances collected", "green"))


if ENVIRONMENT == "production":
    print(emoji.emojize(':hourglass:', use_aliases=True), end=" ")
    print(colored("Waiting to be called", "cyan"))
    schedule.every().hour.at(":00").do(piebot, pairs=pair_list)

    while True:
        schedule.run_pending()
        time.sleep(1)

else:
    piebot(pairs=pair_list)
