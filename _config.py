# The list of coin pairs you want to trade with
pair_list = [
    ("ADA", "ADA_USDT"),
    ("ALGO", "ALGO_USDT"),
    ("ATOM", "ATOM_USDT"),
    ("BTC", "BTC_USDT"),
    ("CRO", "CRO_USDT"),
    ("DOT", "DOT_USDT"),
    ("ETH", "ETH_USDT"),
    ("LTC", "LTC_USDT"),
    ("SHIB", "SHIB_USDT"),
    ("XLM", "XLM_USDT"),
    ("XRP", "XRP_USDT")
]

# How much USDT do you want to keep as a reserve
usdt_reserve = 25

# Sets the minimum and maximum order values, so we don't eat into our USDT balance too quickly
min_order_value = 0.25
max_order_value = 0.50
