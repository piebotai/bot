# The list of coin pairs you want to trade with
pair_list = [
    ("ADA", "ADA_USDT", 1),
    ("ALGO", "ALGO_USDT", 2),
    ("ATOM", "ATOM_USDT", 2),
    ("BTC", "BTC_USDT", 6),
    ("CRO", "CRO_USDT", 3),
    ("DOT", "DOT_USDT", 3),
    ("ETH", "ETH_USDT", 5),
    ("LTC", "LTC_USDT", 5),
    ("SHIB", "SHIB_USDT", 0),
    ("XLM", "XLM_USDT", 1),
    ("XRP", "XRP_USDT", 1)
]

# How much USDT do you want to keep as a reserve
usdt_reserve = 25

# Sets the minimum and maximum order values, so we don't eat into our USDT balance too quickly
min_order_value = 0.25
max_order_value = 0.50
