environment = "dev"
api_key = "xxx"
api_secret = "xxx"

# The list of coin pairs you want to trade with
pair_list = [
    ("ADA", "ADAUSDT"),
    ("ALGO", "ALGOUSDT"),
    ("ATOM", "ATOMUSDT"),
    ("BNB", "BNBUSDT"),
    ("BTC", "BTCUSDT"),
    ("DOT", "DOTUSDT"),
    ("ETH", "ETHUSDT"),
    ("LTC", "LTCUSDT"),
    ("XLM", "XLMUSDT"),
    ("XRP", "XRPUSDT")
]

# How much USDT do you want to keep as a reserve. This is a percentage of the total portfolio balance
# 0.05 = 5%
# 0.15 = 15%
usdt_reserve = 0.05

# Sets the minimum and maximum order values, so we don't eat into our USDT balance too quickly
min_order_value = 0.25
max_order_value = 0.50
