import logging
from lib import Trader

# Global logging setup
# www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3


def main():
    # account info. PASTE YOUR KEYS HERE.
    api_key = ''
    secret_key = ''
    passphrase = ''

    # currency and coin size
    interest_currency = ['LTC', 'USD']  # interested currency
    size = 0.1  # coin size per trade
    currency = 'LTC-USD'  # the currency for trading

    # initial check parameter, for safety purpose
    value_limit = 400  # total amt of value in account limit
    percent_remain_limit = 0.90  # percentage of
    # value remained limit
    size_limit = 1  # coin size limit

    # moving average parameters
    granularity = 3600  # e.g., 3600=an hour, some values are
    # weird (100, etc). We probably use 60 (1 min), 300 (5 min),
    # 1800(30min), 3600(1 hr)
    num_buckets = 200  # total number of buckets we are
    # interested in
    term_n = 60  # the number of buckets that is used to
    # calculate the ema, important parameter to determine how sensitive and
    # global of the moving average, i.e., the smallest, the more senstive
    # to the latest price
    macd_short_n = 12  # default
    macd_long_n = 26  # default

    # trade options
    trade_option_buy = 2
    trade_option_sell = 3

    # Trader
    trader = Trader(api_key=api_key,
                    secret_key=secret_key,
                    passphrase=passphrase,
                    interest_currency=interest_currency,
                    size=size,
                    currency=currency,
                    value_limit=value_limit,
                    percent_remain_limit=percent_remain_limit,
                    size_limit=size_limit,
                    granularity=granularity,
                    term_n=term_n,
                    macd_short_n=macd_short_n,
                    macd_long_n=macd_long_n,
                    trade_option_buy=trade_option_buy,
                    trade_option_sell=trade_option_sell
                    )
    trader.trade()

if __name__ == '__main__':
    main()
