import logging
from lib import Strategier
from lib.utils import *
from __future__ import division


class SellStrategier(Strategier):
    """
    Provide algorithms and rules to determine if we should sell. 
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n,
                 macd_short_n, macd_long_n, time_str
                 ):
        Strategier.__init__(self, army, currency, granularity,
                            num_buckets, term_n, macd_short_n, macd_long_n,
                            time_str)
        # logger
        self.logger = setup_logger(__name__, 'logs/%s_log.log' % time_str)

    def should_sell(self, buy_order, option=1):
        """
        To determine if a stock should sell or not based on the buy order info
        """
        if option == 1:
            return self._determine_by_ema(buy_order)
        elif option == 2:
            return self._determine_by_macd(buy_order)
        elif option == 3:
            return (self._determine_by_macd(buy_order) or self._determine_by_gain_percentage(buy_order))

        return False

    def should_resell(self, buy_order):
        """
        To determine if resell even the sell operation fails. If the selling price after deduction from the take fee (0.25%) is bigger than buying price, then return True.

        TODO: improve it
        """
        # taker percentage
        taker_fee = 0.0025

        # Buy price & current price
        buy_price = float(buy_order['price'])
        price = self.army.get_currency_price(self.currency)

        return price * (1 - taker_fee) > buy_price

    def _determine_by_ema(self, buy_order):
        """
        Determine if we should buy in based on exponetial moving average rule.
        """
        # Buy price
        buy_price = float(buy_order['price'])

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        ema = self._get_cloest_ema(self.term_n)

        # log
        self.logger.info('Simple EMA: price:$%s, ema:$%s' % (price, ema))

        # return True
        # return (price < ema) and (price > buy_price)
        return (price < ema)

    def _determine_by_macd(self, buy_order):
        """
        Determine if we should sell based on MACD
        """
        # Buy price
        buy_price = float(buy_order['price'])

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        short_macd_ema, long_macd_ema = self._get_macd_ema()

        # log
        self.logger.info('MACD: short ema:$%s, long ema:$%s' %
                         (short_macd_ema, long_macd_ema))

        # return. We cannot use price> buy_price because we may run into infinte while loop for sell. Well, if we assume the stock is always going up, then price > buy_price would make sense, but it will takes a long time (e.g., one day) to wait for cycle to complete.
        # return (short_macd_ema < long_macd_ema) and (price > buy_price)
        return (short_macd_ema < long_macd_ema)

    def _determine_by_gain_percentage(self, buy_order, percentage=0.02):
        """
        Determine if we should sell based on gain percentage.

        :params buy_order: the buy order
        :params percentage: the minimal gain percentage
        """
        # Buy price
        buy_price = float(buy_order['price'])

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # calculate the percentage
        gain_percentage = (price - buy_price) / buy_price

        return gain_percentage > percentage
