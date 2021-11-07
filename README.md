PieBot is a DCA (Dollar Cost Averaging) cryptocurrency trading bot, built with Python, for the [Crypto.com Exchange](https://crypto.com/exch/wha692z6ba).

## Table of Contents

- [How It Works](#how-it-works)
	- [Buy](#buy)
	- [Rebalance](#rebalance)
	- [Minimum Order Values](#minimum-order-values)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
	- [Config File](#config-file)
		- [environment](#environment)
		- [api_key](#api_key)
		- [api_secret](#api_secret)
		- [pair_list](#pair_list)
		- [buy_frequency](#buy_frequency)
		- [rebalance_frequency](#rebalance_frequency)
		- [rebalance_threshold](#rebalance_threshold)
		- [buy_order_value](#buy_order_value)
		- [usdt_reserve](#usdt_reserve)
	- [Operation](#operation)
		- [Running PieBot](#running-piebot)
		- [Dev Mode](#dev-mode)
	- [Updating](#updating)
- [Disclaimer](#disclaimer)
- [Donate](#donate)

## How It Works

PieBot is designed to purchase small amounts of your enabled cryptocurrencies at regular intervals, and also aims to keep your holdings the same value by selling over-performers, and buying more of the under-performers.

Simply put, imagine your portfolio as a pie chart. Each slice of the pie represents a cryptocurrency. PieBot aims to keep all slices the same size. Hence PieBot!

PieBot achieves this by running two tasks at different intervals:

### Buy

The Buy task simply buys a set amount of each of your enabled coins.

The value PieBot buys for each coin is set in the `_config.py` file using the `buy_order_value` environment variable. This can be adjusted to meet the needs of your strategy, as well as the frequency at which this task runs, using the `buy_frequency` environment variable.

If there is not enough USDT to complete the whole order, PieBot will skip the task and wait until it is called again.

### Rebalance

The Rebalance task tries to keep all the values of your holdings the same, by selling coins whose values are over the average, and using those profits to buy more of the coins that are below the average.

PieBot will ignore any enabled coin pairs that have a balance of 0.

PieBot will first run through the sell orders, then the buy orders. This is to ensure there is enough USDT available when it comes to the buy orders, just in case the `usdt_reserve` isn't adequate.

The frequency at which this task runs is configured using the `rebalance_frequency` environment variable.

PieBot has no maximum order value for buying or selling a holding to bring it back on target.

### Minimum Order Values

Each order placed during the Buy and Rebalance task is subject to a minimum order value.

This value cannot be changed, and is set at `0.25` USDT per coin. The reasons for this are as follows:

- Firstly, due to the nature of quantity and price decimal points, some coins have a much larger minimum order value than others. For exmaple, `ATOM` only has 2 decimal places for quantity, so `0.01` (the smallest amount) of `ATOM` works out at `0.133 USDT`*. In this example, if an order was placed with a value of `0.12` or lower, the order would be rejected by the exchange, which would make it hard for PieBot to keep your holdings balanced
- Secondly, it prevents situations where the bot might want to rebalance a coin pair if it's `0.01 USDT` over target, which is not an efficent use of trading fees

_*Price correct at time of writing_

## Requirements
- [Git](https://git-scm.com/download) `2.x`
- [Python](https://www.python.org/downloads) `3.9`
- [Pip](https://pypi.org/project/pip) `21.x`

## Installation

Run these commands to get PieBot's code, and to prepare your environment for setup and usage:

```
git clone https://github.com/piebotai/bot.git PieBot
cd PieBot
sh init.sh
```

`init.sh` is a simple Shell script that handles the set-up for you. It will put you on the correct Git branch, pull down the latest code, and install the required Pip packages:

- [Schedule](https://pypi.org/project/schedule)
- [Termcolor](https://pypi.org/project/termcolor)

## Usage

### Config File

PieBot's settings are handled through a `_config.py` file in the root of the project. This file is not included when you clone the project, as it contains sensitive information, so you'll need to set it up yourself.

In the root of the project is a `_config-example.py` file. Copy and paste this file, and rename the pasted file to `_config.py`.

You should now have two config files in your project **with exactly the same code in them**:

```
_config.py
_config-example.py
```

For now, you can safely ignore `_config-example.py`. Open `_config.py` in your text editor of choice, and configure your environment accordingly:

---

#### environment

This can be one of two options:

- `production` - Real trades with real money
- `dev` - PieBot's logic runs, but no real trades are submitted

**Default value** - `production`

---

#### api_key

The API key for your Crypto.com Exchange account.

---

#### api_secret

The API secret for your Crypto.com Exchange account.

---

#### pair_list

A comma separated list of the coin pairs you want PieBot to trade. For example, this is how we would enable BTC trading using USDT:

`("BTC", "BTC_USDT")`

You will need to define both the token you want to trade, and the whole coin pair, just like above.

---

#### buy_frequency

Set after how many hours the **Buy** task should repeat.

**Default value** - `6`

---

#### rebalance_frequency

Set after how many hours the **Rebalance** task should repeat.

You can stop the Rebalance task from running by setting the value as `0`. In this situation, PieBot would just run the Buy task, and nothing else.

**Default value** - `1`

---

#### rebalance_threshold

Sets the desired price deviation a coin must meet before it is rebalanced.

By specifying a target percentage, rather than just requiring the deviation to be greater than or equal to the minimum order value, you dramatically reduce the number of trades PieBot completes in any given cycle, which can help reduce fees.

For example, if `rebalance_threshold` is set to `0.025`, then each coin pair must be greater than or equal to 2.5% above or below the target coin price. So, coins that are within the 0% - 2.49999...% window will not be rebalanced in this cycle.

The value reflects a percentage, and should be between `0` and `1`.

For example, 5% = `0.05`, 15% = `0.15` etc.

**Default value** - `0.03`

---

#### buy_order_value

The USDT value that PieBot will buy for each enabled coin pair in the Buy task.

For example, with 10 enabled coin pairs, and a `buy_order_value` of `0.5`, the Buy task would use a total of `5.00 USDT` - `0.5 * 10` each time it is run.

**Default value** - `0.50`

---

#### usdt_reserve

This value tells PieBot how much USDT it should keep aside to not trade with.

The value reflects a percentage, and should be between `0` and `1`.

For example, 5% = `0.05`, 15% = `0.15` etc.

**It is strongly recommended that you don't set this value as 0.** It's a good idea to leave some USDT in reserve, so PieBot has some equity available should it need it.

**Default value** - `0.02`

---

### Operation

It is strongly recommended running PieBot with a process manager such as [PM2](https://pm2.keymetrics.io).

#### Running PieBot

To start PieBot without PM2, simply run:

```python
python3 PieBot.py
```

To start PieBot with PM2, run the above command first to make sure everything is working. If no errors come back, and you see the "Waiting to be called" message, stop the bot and start it again with PM2:

```python
pm2 start PieBot.py --name PieBot --interpreter=python3
```

Once it is running, you can view the logs for that PM2 process like so:

```
pm2 logs PieBot
```

#### Dev mode

By setting `environment = "dev"` in your `_config.py` file, you can run PieBot without placing any real world trades. This is a good way of running the bot for the first time to ensure everything is working, without the risk of placing real trades for real money.

As PieBot is split into two distinct tasks; [Buy](#buy) and [Rebalance](#rebalance), you will need to specify which task you want to run by using one of these commands:

```
python3 PieBot.py Buy
python3 PieBot.py Rebalance
```

When in dev mode, PieBot uses exactly the same logic as if you were running the bot in the real world. The bot attempts to connect to your account through your API key, it will collect your coin balances and work everything out it needs to. You will even see exactly the same console output. The only difference being that orders aren't actually placed.

### Updating

PieBot updates are pushed directly to this Git repository, so a simple `git pull` on the `main` branch is normally all that is required to run the latest version of the bot. Luckily there is a little script file you can run that handles it for you.

**Ensure you have stopped PieBot before updating it, and restart it again once you have updated.**

```
sh update.sh
```

## Disclaimer

This bot is built for private use only. Whilst you are free to use the bot for your own trading purposes, by doing so you acknowledge that its owners, developers, and/or anyone involved with the project is not responsible for any damages or losses as a result.

The trading strategy used in this bot is experimental and is constantly changing.

Please only invest money you are prepared to lose. Prices go up as well as down, and you may get back less than you put in.

## Donate 🥧

If you love PieBot as much as I do, please consider sending a small donation to keep the project going:

```
CRO - cro159uyrxk7zqjrd6e3zhsljhqt553nv2p75x8q2c
XLM - GDFN6UFSQ5Q7IZCN3FVI6VEV2SEVZ7TONSY4TSLOCYIKUOAB2KB7I4CI
XRP - rJT1ZwBqgRmZQbPUD3ppfUWwpmxPd77BW1
```
