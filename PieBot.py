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
    print(colored("Collecting current balances", "cyan"))


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
    rebalance(pairs=pair_list)
