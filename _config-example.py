environment = "production"
api_key = "xxx"
api_secret = "xxx"

# Set the stablecoin you want to trade with
stablecoin = "USDT"

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
    ("XLM", "XLM_USDT"),
    ("XRP", "XRP_USDT")
]

# Sets after how many hours each task should repeat
buy_frequency = 6
rebalance_frequency = 1

# The value in your chosen stablecoin that PieBot will buy for each enabled coin pair in the "Buy" task
buy_order_value = 0.50

# How much of your chosen stablecoin do you want to keep as a reserve. This is a percentage of the total portfolio balance
# 0.05 = 5%
# 0.15 = 15%
stablecoin_reserve = 0.02
