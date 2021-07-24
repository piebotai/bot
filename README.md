PieBot is an automated cryptocurrency trading bot, built with Python, for the [Crypto.com Exchange](https://crypto.com/exch/wha692z6ba).

## Table of Contents

- [How It Works](#how-it-works)
  - [Example](#example)
  - [Regular Deposits](#regular-deposits)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
    - [Config File](#config-file)
    - [Operation](#operation)
    - [Updating](#updating)
- [Disclaimer](#disclaimer)
- [Donate](#donate)

## How It Works

PieBot is a very simple Dollar Cost Averaging (DCA) bot for the [Crypto.com Exchange](https://crypto.com/exch/wha692z6ba).

PieBot is designed to purchase small amounts of your enabled cryptocurrencies at regular intervals, and also aims to keep your holdings the same value by selling over-performers, and buying more of the under-performers.

Simply put, imagine your portfolio as a pie chart. Each slice of the pie represents a cryptocurrency. PieBot aims to keep all slices the same size. Hence PieBot!

PieBot achieves this by running two tasks at different intervals:

### Buy

The Buy task simply buys a set amount of each of your enabled coins.

The value PieBot buys for each coin is set in the `_config.py` file using the `max_buy_order_value` environment variable. This can be adjusted to meet the needs of your strategy, as well as the frequency at which this task runs, using the `buy_frequency` environment variable.

If there is not enough USDT to complete the whole order, PieBot will skip the task and wait until it is called again.

### Rebalance

The Rebalance task tries to keep all the values of your holdings the same, by selling coins whose values are over the average, and using those profits to buy more of the coins that are below the average.

The maximum value PieBot buys for each coin is set in the `_config.py` file using the `max_rebalance_order_value` environment variable. This can be adjusted to meet the needs of your strategy, as well as the frequency at which this task runs, using the `rebalance_frequency` environment variable.

PieBot has no maximum order value for selling a holding to bring it back on target, to ensure as much profit is secured as possible.

## Requirements
- [Git](https://git-scm.com/download) `2.x`
- [Python](https://www.python.org/downloads) `3.9`
- [Pip](https://pypi.org/project/pip) `21.x`

## Installation

Run these commands to get PieBot's code, and to prepare your environment for setup and usage:

```
git clone https://github.com/piebotai/bot.git PieBot
cd PieBot
git fetch --all
git checkout main
git pull origin main
```

Install the required packages:

```
pip3 install schedule
pip3 install termcolor
```

## Usage

### Config File

PieBot's settings are handled through a `_config.py` file in the root of the project. This file is not included when you clone the project, as it contains sensitive information, so you'll need to set it up yourself.

In the root of the project is a `_config-example.py` file. Copy and paste this file, and rename the pasted file to `_config.py`.

You should now have two config files in your project **with exactly the same code in them**:

```
_config.py
_config-example.py
```

For now, you can now safely ignore `_config-example.py`. Open `_config.py` in your text editor of choice, and configure your environment accordingly:

#### environment

This can be one of two options:

- `production` - Real trades with real money
- `dev` - PieBot's logic runs, but no real trades are submitted

**Default value** - `production`

#### api_key

The API key for your Crypto.com Exchange account

#### api_secret

The API secret for your Crypto.com Exchange account

#### pair_list

A comma separated list of the coin pairs you want PieBot to trade. For example, this is how we would enable BTC trading using USDT:

`("BTC", "BTC_USDT")`

You will need to define both the token you want to trade, and the whole coin pair, just like above.

#### buy_frequency

Set after how many hours the **Buy** task should repeat.

**Default value** - `8`

#### rebalance_frequency

Set after how many hours the **Rebalance** task should repeat.

**Default value** - `1`

#### usdt_reserve

This value tells PieBot how much USDT it should keep aside to not trade with. The value reflects a percentage, and should be between `0` and `1`.

For example, 5% = `0.05`, 15% = `0.15` etc.

**It is strongly recommended that you don't set this value as 0.** It's a good idea to leave some USDT in reserve, so PieBot has some equity available should it need it.

**Default value** - `0.05`

#### max_buy_order_value

The maximum buy value an order should be in the **Buy** task for PieBot to execute it.

**Default value** - `0.50`

#### max_rebalance_order_value

The maximum buy value an order should be in the **Rebalance** task for PieBot to execute it. PieBot has no upper limit when selling to rebalance orders.

**Default value** - `0.25`

### Operation

It is strongly recommended running PieBot with a process manager such as [PM2](https://pm2.keymetrics.io).

#### Running PieBot

To start PieBot without PM2, simply run:

```python
python3 PieBot.py
```

To start PieBot with PM2, run the above command first to make sure everything is working. If no errors come back, and you see the "Waiting to be called" message, stop the bot and start it again with PM2:

```python
pm2 start PieBot.py --name PieBot --interpreter=python3 --time
```

### Updating

PieBot updates are pushed directly to this Git repository, so a simple `git pull` on the `main` branch is normally all that is required to run the latest version of the bot.

Ensure you have stopped PieBot before updating it, and restart it again once you have updated.

```
git reset HEAD --hard
git checkout main
git pull origin main
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
