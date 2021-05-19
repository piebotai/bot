import emoji
import sys
from termcolor import colored
import time

from _config import *


# Checks everything is in order before the bot runs
def pre_flight_checks():
    print(emoji.emojize(':rocket:', use_aliases=True), end=" ")
    print(colored("Performing pre-flight checks", "cyan"))

    # Checks whether the trading pairs have been defined, and if there is enough to begin trading
    try:
        environment
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your environment is missing from the config file", "red"))
        sys.exit()

    # Checks whether the API key and API secret have been defined
    try:
        api_key and api_secret
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your API key and API secret are missing from the config file", "red"))
        sys.exit()

    # Checks whether the trading pairs have been defined, and if there is enough to begin trading
    try:
        pair_list
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your trading coin pairs are missing from the config file", "red"))
        sys.exit()
    else:
        if len(pair_list) < 1:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("You need to use at least one coin pair", "red"))
            sys.exit()

    # Checks whether the USDT reserves amount has been defined
    try:
        usdt_reserve
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your USDT reserve amount is missing from the config file", "red"))
        sys.exit()
    else:
        if usdt_reserve < 0:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("You need to define a valid USDT reserve. If you don't want to use a reserve, set the value as 0", "red"))
            sys.exit()
        elif usdt_reserve > 80:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("Your USDT reserve must be 80% or lower", "red"))
            sys.exit()

    # Checks whether the minimum order value has been defined and is valid
    try:
        min_order_value
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your minimum order value is missing from the config file", "red"))
        sys.exit()
    else:
        if min_order_value < 0.25:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("Your minimum order value must be 0.25 or greater", "red"))
            sys.exit()

    # Checks whether the maximum order value has been defined and is valid
    try:
        max_order_value
    except NameError:
        print(emoji.emojize(':x:', use_aliases=True), end=" ")
        print(colored("Your maximum order value is missing from the config file", "red"))
        sys.exit()
    else:
        if max_order_value < min_order_value:
            print(emoji.emojize(':x:', use_aliases=True), end=" ")
            print(colored("Your maximum order value cannot be smaller than your minimum order value", "red"))
            sys.exit()
