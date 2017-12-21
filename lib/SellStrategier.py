import logging
from lib import Strategier
from lib.utils import *

logger = setup_logger(__name__, 'logs/log.log')


class SellStrategier(Strategier):
    """
    Provide algorithms and rules to determine if we should sell. 
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n):
        Strategier.__init__(self, army, currency, granularity,
                            num_buckets, term_n)

    def should_sell(self, buy_order, option=1):
        """
        To determine if a stock should sell or not based on the buy order info
        """
        if option == 1:
            return self._determine_by_ema(buy_order)

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
        ema = self._get_closest_ema(self.granularity, self.num_buckets,
                                    self.term_n)

        # log
        logger.info('price:$%s, ema:$%s' % (price, ema))

        return True
        #return (price < ema) and (price > buy_price)
