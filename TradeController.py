from utils import *
import time

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

    def trade_by_ema_limit(self, 
                            size=0.01,
                            granularity=300, 
                            num_buckets=200,
                            term_n=50, 
                            ):
        """
        Trade using exponential moving average (EMA) in a limit fashion. We are assuming doing one trade (cycle) at a time. A cycle is defined as a-buy-a-sell.
        """

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        ema = self._get_closest_ema(granularity, num_buckets, term_n)

        # check if orderbook is empty, for now, just allow one order pair at a time        
        if price >= ema:
            order = self.army.buy()      

        # wait until buy-order is filled
        while not self._is_order_filled(id=order['id']):
            time.sleep(2) # pause for x second
            break

        # once the buy order is filled, put a sell order
        order = self._create_sell_order(order)

        # wait until the sell-order is filled
        while not self._is_order_filled(id=order['id']):
            time.sleep(2)
            break



       
        
    def _is_order_filled(self, id):
        """
        Check if an order is filled

        :params id: the id of an order
        """
        info = self.army.get_order(id)
        print(info)
        if info['status'] == 'done':
            return True
        else:
            return False


    def _create_sell_order(self, buy_order, gain=0.1):
        """
        Create a sell order based on info of a buy_order

        :params gain: the percent gain that is expected to have
        """
        price = float(buy_order['price']) * (1 + gain)
        product_id = buy_order['product_id']
        size = float(buy_order['size'])
        order = self.army.sell(price=price, size=size)
        return order


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






	
