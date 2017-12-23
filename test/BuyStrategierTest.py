# TODO: fix the path issue by writing python setup.py script:
# https://stackoverflow.com/questions/9383014/cant-import-my-own-modules-in-python
import sys
sys.path.append("..")

import unittest
import logging
from lib.utils import *

from lib import GdaxArmy, BuyStrategier, SellStrategier

class BuyStrategierTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        # Overriding original test case __init__
        super(BuyStrategierTest, self).__init__(*args, **kwargs)
        # self.gen_stubs()

        # Please hide if not in testing
        api_key = ''
        secret_key = ''
        passphrase = ''

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
        self.buyStrategier = BuyStrategier(self.army, currency, granularity,
                                           num_buckets, term_n, macd_short_n, macd_long_n)

    def testOne(self):
        self.buyStrategier.should_buy(option=1)

    def testTwo(self):
        self.buyStrategier.should_buy(option=2)

def main():
    unittest.main()

if __name__ == '__main__':
    main()
