environment = "production"
api_key = "xxx"
api_secret = "xxx"

# Set the type of stable coin your will trade with (USDC, USDT, TUSD etc.)
stable_coin = "USDC"

# The list of coin pairs you want to trade with
pair_list = [
    ("ADA", "ADA_" + stable_coin),
    ("ALGO", "ALGO_" + stable_coin),
    ("ATOM", "ATOM_" + stable_coin),
    ("BTC", "BTC_" + stable_coin),
    ("CRO", "CRO_" + stable_coin),
    ("DOT", "DOT_" + stable_coin),
    ("ETH", "ETH_" + stable_coin),
    ("LTC", "LTC_" + stable_coin),
    ("XLM", "XLM_" + stable_coin),
    ("XRP", "XRP_" + stable_coin)
]

# Sets after how many hours each task should repeat
buy_frequency = 6
rebalance_frequency = 1

# The required value deviation before the coin is rebalanced.  This is a percentage
# 0.05 = 5%
# 0.15 = 15%
rebalance_threshold = 0.03

# The USDT value that PieBot will buy for each enabled coin pair in the "Buy" task
buy_order_value = 0.50

# How much USDT do you want to keep as a reserve. This is a percentage of the total portfolio balance
# 0.05 = 5%
# 0.15 = 15%
stable_coin_reserve = 0.02
