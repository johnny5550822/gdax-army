class Strategier():
    """
    The parent of the buy and sell strategiers.
    """

    def __init__(self, army, currency, granularity, num_buckets, term_n,
                 macd_short_n, macd_long_n, time_str
                 ):
        # basic
        self.army = army
        self.currency = currency

        # exponential moving average parameters
        self.granularity = granularity  # e.g., 3600=an hour, some values are
        # weird (100, etc). We probably use 60 (1 min), 300 (5 min),
        # 1800(30min), 3600(1 hr)
        self.num_buckets = num_buckets  # total number of buckets we are
        # interested in
        self.term_n = term_n  # the number of buckets that is used to
        # calculate the ema, important parameter to determine how sensitive and
        # global of the moving average, i.e., the smallest, the more senstive
        # to the latest price

        # MACD parameters
        self.macd_short_n = macd_short_n
        self.macd_long_n = macd_long_n

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

    def _get_exponential_moving_average(self, n=10):
        """
        return the n-day exponential moving average

        :params n: the size of the moving window (number or periods
                        involved)
                        10-20 short-term trends
                        50 mid-term trends
                        200 long-term trends        
        """
        time_, low_, high_, mean_, open_, close_, \
            volume_ = self.army.get_trade_trends(currency=self.currency,
                                                 granularity=self.granularity,
                                                 num_buckets=self.num_buckets)
        return close_.ewm(span=n).mean()

    def _get_cloest_ema(self, n=10):
        """
        Get the cloest ema. 
        """
        # Get the cloest ema
        ema = self._get_exponential_moving_average(n)
        return ema.iloc[-1]

    def _get_macd_ema(self):
        """
        Get the macd short and long EMA.

        https://www.youtube.com/watch?v=E3KP1WyLITY&index=11&list=PL0I_pt3KKS0
        zT0y7gW2CLrSP1xTPYRMK_
        """

        # Get the cloest ema for short ema
        short_ema = self._get_cloest_ema(self.macd_short_n)

        # Get the cloest ema for long ema
        long_ema = self._get_cloest_ema(self.macd_long_n)
        return short_ema, long_ema
