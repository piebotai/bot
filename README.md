PieBot is an automated cryptocurrency trading bot, built with Python, for the [Crypto.com Exchange](https://crypto.com/exch/wha692z6ba).

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
    - [Config File](#config-file)
    - [Operation](#operation)
    - [Updating](#updating)
- [Disclaimer](#disclaimer)
- [Donate](#donate)

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
pip3 install emoji
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

#### usdt_reserve

This value tells PieBot how much USDT it should keep aside to not trade with. The value reflects a percentage, and should be between `0` and `1`.

For example, 5% = `0.05`, 15% = `0.15` etc.

**It is strongly recommended that you don't set this value as 0.** It's a good idea to leave some USDT in reserve, so PieBot has some equity available should it need it.

**Default value** - `0.05`

#### min_order_value

The minimum value an order should be for PieBot to execute it.

**It is strongly recommended to leave this value at 0.25**, which has been set as the default for two reasons:

- Firstly, due to the nature of quantity and price decimal points, some coins have a much larger minimum order value than others. For exmaple, `ATOM` only has 2 decimal places for quantity, so `0.01` (the smallest amount) of `ATOM` works out at `0.133 USDT`*
- Secondly, it prevents situations where the bot might want to rebalance a coin pair if it's `0.01 USDT` over target, which is not an efficent use of trading fees

**Default value** - `0.25`

_*Price correct at time of writing_

#### max_order_value

The maximum **buy** value an order should be for PieBot to execute it. PieBot has no upper limit for rebalance orders, but it does adhere to `min_order_value`.

**Default value** - `0.50`

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

## Donate

If you love PieBot as much as I do, please consider sending a small donation to keep the project going:

```
CRO - cro159uyrxk7zqjrd6e3zhsljhqt553nv2p75x8q2c
XLM - GDFN6UFSQ5Q7IZCN3FVI6VEV2SEVZ7TONSY4TSLOCYIKUOAB2KB7I4CI
XRP - rJT1ZwBqgRmZQbPUD3ppfUWwpmxPd77BW1
```
