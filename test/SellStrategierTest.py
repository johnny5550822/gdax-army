# TODO: fix the path issue by writing python setup.py script:
# https://stackoverflow.com/questions/9383014/cant-import-my-own-modules-in-python
import sys
sys.path.append("..")

import unittest
import logging
from lib.utils import *

from lib import GdaxArmy, BuyStrategier, SellStrategier


class SellStrategierTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        # Overriding original test case __init__
        super(SellStrategierTest, self).__init__(*args, **kwargs)
        # self.gen_stubs()

        # Please hide if not in testing
        api_key = '097f67c2c1cb3452f33fcdf143361142'
        secret_key = 'qQvU8RjCksVPF6KtuKMFY+bcgeaSeUlRpLvEdV5L4esiZxwWTVIszuCqXiuYbMVIfWl/NmE1zWqwiFT7xLbz3w=='
        passphrase = 'kznsevl3lgvx3dpk995yzxgvi'

        # parameters
        interest_currency = ['LTC', 'USD']
        currency = 'LTC-USD'
        granularity = 300
        num_buckets = 200
        term_n = 50
        macd_short_n = 12
        macd_long_n = 26

        # api key
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

        # create the trade army
        self.army = GdaxArmy()
        self.interest_currency = interest_currency
        self.army.authenticate(api_key=api_key,
                               secret_key=secret_key, passphrase=passphrase,
                               interest_currency=self.interest_currency,
                               is_sandbox_url=False)

        # strategiers
        self.sellStrategier = SellStrategier(self.army, currency, granularity,
                                             num_buckets, term_n, macd_short_n, macd_long_n)

    def testOne(self):
        buy_order = {}
        buy_order['price'] = 10
        self.sellStrategier.should_sell(buy_order, option=1)

    def testTwo(self):
        buy_order = {}
        buy_order['price'] = 10
        self.sellStrategier.should_sell(buy_order, option=2)


def main():
    unittest.main()

if __name__ == '__main__':
    main()