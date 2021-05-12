environment = "dev"
api_key = "xxx"
api_secret = "xxx"

# The list of coin pairs you want to trade with
pair_list = [
    ("ADA", "ADA_USDT", 5, 1),
    ("ALGO", "ALGO_USDT", 4, 2),
    ("ATOM", "ATOM_USDT", 3, 2),
    ("BTC", "BTC_USDT", 2, 6),
    ("CRO", "CRO_USDT", 5, 3),
    ("DOT", "DOT_USDT", 4, 3),
    ("ETH", "ETH_USDT", 2, 5),
    ("LTC", "LTC_USDT", 2, 5),
    ("SHIB", "SHIB_USDT", 9, 0),
    ("XLM", "XLM_USDT", 5, 1),
    ("XRP", "XRP_USDT", 5, 1)
]

# How much USDT do you want to keep as a reserve
usdt_reserve = 0.05

# Sets the minimum and maximum order values, so we don't eat into our USDT balance too quickly
min_order_value = 0.25
max_order_value = 0.50
