import logging
from lib import Strategier
from lib.utils import *

logger = setup_logger(__name__, 'logs/log.log')


class BuyStrategier(Strategier):
    """
    Provide algorithms and rules to determine if we should buy. 
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n,
                 macd_short_n, macd_long_n
                 ):
        Strategier.__init__(self, army, currency, granularity,
                            num_buckets, term_n, macd_short_n, macd_long_n)

    def should_buy(self, option=1):
        """
        To determine if a stock should buy or not
        """
        if option == 1:
            return self._determine_by_ema()
        elif option == 2:
            return self._determine_by_macd()

        return False

    def _determine_by_ema(self):
        """
        Determine if we should buy in based exponetial moving average rule.
        """

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        ema = self._get_cloest_ema(self.term_n)

        # log
        logger.info('Simple EMA: price:$%s, ema:$%s' % (price, ema))

        # Todo: just simply check price >= ema and decide to buy may be wrong
        # because we don't know if we buy at a very high price (e.gh., the
        # peak), we may have to have a better way to determine if we should
        # excute a buy order. For example, (1) we should determine if the trend
        # of the price is still going up or not (i.e., pass the peak). (2) Or
        # we should let the algorithm to wait from price<=ema to price>=ema,
        # the turning point should be a good price to buy
        return (price >= ema)

    def _determine_by_macd(self):
        """
        Determine if we should buy based on MACD. if short_ema > long_ema, then buy.
        """

        short_macd_ema, long_macd_ema = self._get_macd_ema()

        # log
        logger.info('MACD: short ema:$%s, long ema:$%s' %
                    (short_macd_ema, long_macd_ema))

        return (short_macd_ema >= long_macd_ema)
