import base64
import hashlib
import hmac
import time
import json
import requests
import gdax
import pandas as pd
from lib.utils import *


class GdaxArmy():
    """
    An API object that is built on top of the unofficial Gdax python api:
    https://github.com/danpaquin/gdax-python
    """

    def __init__(self):
        self.client = gdax.PublicClient()
        self.auth_client = None

    def authenticate(self, api_key, secret_key, passphrase,
                     interest_currency, is_sandbox_url=True):
        """
        Authenticate the account.
        """
        if is_sandbox_url:
            api_url = 'https://api-public.sandbox.gdax.com'
        else:
            api_url = 'https://api.gdax.com'
        self.auth_client = gdax.AuthenticatedClient(api_key,
                                                    secret_key,
                                                    passphrase,
                                                    api_url=api_url
                                                    )

        # Get the acounts info
        accts = self.auth_client.get_accounts()
        self.auth_client.accts_dict = {}
        for acct in accts:
            if acct['currency'] in interest_currency:
                self.auth_client.accts_dict[acct['currency']] = acct

    def get_accts_dict(self):
        """
        Return the acct in Gdax info.
        """
        return self.auth_client.accts_dict

    def buy(self, price=1, size=0.01, product_id='LTC-USD',
            post_only=True, **kwargs):
        """
        Perform a buy order. For example buy 0.01 LTC @100 USD
        """
        order = self.auth_client.buy(price=price, size=size,
                                     product_id=product_id,
                                     post_only=post_only, **kwargs)
        return order

    def sell(self, price=10000, size=0.01, product_id='LTC-USD',
             post_only=True, **kwargs):
        """
        Perform a sell order. For example sell 0.01 LTC @ 100USD
        """
        order = self.auth_client.sell(price=price, size=size,
                                      product_id=product_id,
                                      post_only=post_only, **kwargs)
        return order

    def get_fills(self, **kwargs):
        """
        Get fills info for a particular order id or product id.
        """
        return self.auth_client.get_fills(**kwargs)

    def get_order(self, id):
        """
        Get the order info for a particular order.
        """
        return self.auth_client.get_order(id)

    def get_orders(self):
        """
        Get the list of orders.
        """
        return self.auth_client.get_orders()

    def cancel_order(self, id):
        """
        Cancel an order.
        """
        return self.auth_client.cancel_order(id)

    def get_trade_trends(self, currency='LTC-USD', granularity=3600,
                         num_buckets=200
                         ):
        """
        Getting the trade trends in a period of time. A period contains num_buckets of buckets. For example, a period can be 24 hours (defined by granularity); this also indicates there will be num_buckets=24 and each bucket has a time interval of an hour. Each bucket contains several information:

        low: lowest price during the bucket interval
        high: highest price during the bucket interval
        open: first trade in the bucket interval
        close: last trade in the bucket interval
        volume: volume of trading activity during the bucket interval

        :params currency: currency that we are interested in
        :params granularity: unit is second. Amt of time in a bucket
        :params num_buckets: number of buckets
        """
        trades = self.client.get_product_historic_rates(currency,
                                                        granularity=granularity)
        trades = trades[:num_buckets]
        trades = trades[::-1]  # closest time goes last
        df = pd.DataFrame(data=trades)

        # convert time to readable
        df[0] = df[0].apply(unix_timestamp_to_readable)

        # assign
        time_, low_, high_, open_, close_, volume_ = df[0], df[1], df[2], \
            df[3], df[4], df[5]
        mean_ = (low_ + high_) / 2
        return time_, low_, high_, mean_, open_, close_, volume_

    def get_currency_price(self, currency='LTC-USD'):
        """
        Return the current price of a currency.

        :params currency: the currency for exchange
        """
        info = self.client.get_product_order_book(currency, level=1)
        return float(info['asks'][0][0])

    def get_product_trades(self, product_id='LTC-USD'):
        """
        Get the done trades for a particular product.
        """
        return self.client.get_product_trades(product_id=product_id)

    def get_product_order_book(self, product_id='LTC-USD', level=2):
        """
        Get the current existing placed order (but not yet trade).
        """
        return self.client.get_product_order_book(product_id=product_id,
                                                  level=level
                                                  )
