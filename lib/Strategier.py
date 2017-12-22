

class Strategier():
    """
    The parent of the buy and sell strategiers.
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n):
        self.army = army
        self.currency = currency

        # exponential moving average parameters
        self.granularity = granularity  # e.g., 3600=an hour, some values are 
                                        # weird (100, etc). We probably
                                        # use 60 (1 min), 300 (5 min), 
                                        # 1800(30min), 3600(1 hr)
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
        ema = self._get_exponential_moving_average(df=close_,
                                                       n=n)
        ema = ema.iloc[-1]
        return ema

    def _get_simple_moving_average(self, df, n=10):
        """
        return the simple moving average.

        :params df: dataframe or series with one column
        :params n: the size of the moving window (number or periods
                        involved)
                        10-20 short-term trends
                        50 mid-term trends
                        200 long-term trends
        """
        return df.rolling(n).mean()

    def _get_exponential_moving_average(self, df, n=10):
        """
        return the n-day exponential moving average

        :params df: dataframe or series with one column
        :params n: the size of the moving window (number or periods
                        involved)
                        10-20 short-term trends
                        50 mid-term trends
                        200 long-term trends        
        """
        return df.ewm(span=n).mean()