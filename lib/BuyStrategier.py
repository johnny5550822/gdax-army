import logging
from lib import Strategier

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)


class BuyStrategier(Strategier):
    """
    Provide algorithms and rules to determine if we should buy. 
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n):
        Strategier.__init__(self, army, currency, granularity,
                            num_buckets, term_n)

    def should_buy(self, option=1):
        """
        To determine if a stock should buy or not
        """
        if option == 1:
            return self._determine_by_ema()

        return False

    def _determine_by_ema(self):
        """
        Determine if we should buy in based on exponetial moving average rule.
        """

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        ema = self._get_closest_ema(self.granularity, self.num_buckets,
                                    self.term_n)

        # log
        logger.info('price:$%s, ema:$%s' % (price, ema))

        # Todo: just simply check price >= ema and decide to buy may be wrong
        # because we don't know if we buy at a very high price (e.gh., the
        # peak), we may have to have a better way to determine if we should
        # excute a buy order. For example, (1) we should determine if the trend
        # of the price is still going up or not (i.e., pass the peak). (2) Or
        # we should let the algorithm to wait from price<=ema to price>=ema,
        # the turning point should be a good price to buy
        return (price >= ema)
