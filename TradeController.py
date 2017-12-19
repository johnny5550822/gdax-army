from utils import *

class TradeController():
    """
    Trade controller (bot) that handles all the trading algorithm.
    """

    def __init__(self, acct_id, api_key, secret_key, 
                 passphrase, currency='LTC-USD'):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

        self.currency = currency
        self.army = GdaxArmy()
        self.army.authenticate(api_key=api_key, 
                                secret_key=secret_key, passphrase=passphrase, 
                                is_sandbox_url=False)
        self.orderbook={}


    def trade_by_ema_limit(self, granularity=300, 
                            num_buckets=200,
                            short_term_n=10, 
                            mid_term_n=50, 
                            long_term_n=200
                            ):
        """
        Trade using exponential moving average (EMA) in a limit fashion. We are assuming doing one trade (cycle) at a time. A cycle is defined as a-buy-a-sell.
        """
        size = 0.01
        is_buying_stage = False # flag to indicate if it is in buying stage

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        ema = self._get_closest_ema(granularity, num_buckets,mid_term_n)

        # if there is no traction in orderbook 
        #if len(self.orderbook):
        #    pass
        #if price >= ema:
            #self.army.buy()      

        # wait until the buy order is filled


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






	
