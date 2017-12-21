

class Strategier():
    """
    The parent of the buy and sell strategiers.
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n):
        self.army = army
        self.currency = currency

        # exponential moving average parameters
        self.granularity = granularity  # 300s = 5 min
        self.num_buckets = num_buckets
        self.term_n = term_n  # important parameter to determine how sensitive
                             # and global of the moving average, i.e., the
                             # smallest, the more senstive to the latest price

    def _get_closest_ema(self, granularity, num_buckets, n):
        """ 
        calculate the most recent(closest) exponential moving average (ema).
        """
        time_, low_, high_, mean_, open_, close_, \
            volume_ = self.army.get_trade_trends(currency=self.currency,
                                                 granularity=granularity,
                                                 num_buckets=num_buckets)

        # calculate the EMA and obtain the last ema
        ema = self.army.get_exponential_moving_average(df=close_,
                                                       n=n)
        ema = ema.iloc[-1]
        return ema
