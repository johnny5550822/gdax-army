from utils import *
import time
import logging

logger = logging.getLogger(__name__)
ch = logging.StreamHandler()
logger.addHandler(ch)

class TradeController():
    """
    Trade controller (bot) that handles all the trading algorithm.
    """

    def __init__(self, api_key, secret_key, passphrase, 
                 interest_currency=['LTC', 'USD'],
                 size=0.01, currency='LTC-USD', sell_gain=0.01,
                 value_limit=470, percent_remain_limit=0.90, size_limit=0.1,
                 granularity=300, num_buckets=200, term_n=60
                 ):
        # logger
        logger.info('')
        logger.info('---------------Trade controller---------------')

        # api key
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

        # create the trade army
        self.army = GdaxArmy()
        self.interest_currency =  interest_currency
        self.army.authenticate(api_key=api_key, 
                                secret_key=secret_key, passphrase=passphrase, 
                                interest_currency=self.interest_currency,
                                is_sandbox_url=False)

        # Get initial acct summary
        self.acct_summary = self._get_acct_summary()

        # for buy and sell
        self.size = size #coin size per trade
        self.currency = currency
        self.sell_gain = sell_gain #how much I want to gain; TODO: this number is quite arbitrary, I think we should use some way to calculate this number. For example, we can look at the past period ema the maximum price to determine the gain

        # initial check parameter, for safety purpose
        self.value_limit = value_limit # total amt of value in account limit
        self.percent_remain_limit = percent_remain_limit # percentage of 
                                                         # value remained limit
        self.size_limit = size_limit # coin size limit   

        # exponential moving average parameters
        self.granularity = granularity #300s = 5 min
        self.num_buckets = num_buckets
        self.term_n = term_n #important parameter to determine how sensitive 
                            #and global of the moving average, i.e., the 
                            #smallest, the more senstive to the latest price

        # log the configuration
        logger.info("Initial Account Summary:%s" %self.acct_summary)


    def trade_by_ema_limit(self):
        """
        Trade using exponential moving average (EMA) in a limit fashion. We are assuming doing one trade (cycle) at a time. A cycle is defined as a-buy-a-sell.

        Note: for now, the algorithm will first&end CANCELL all the existing orders, which may cause 'leftover' in digital coin (e.g., LTC).
        """
        logger.info('########## Trade using Expo. moving average ##########')

        # security check to make sure we will start investment    
        if self._pass_initial_check():

            # Clean up all the existing order first
            self._clean_all_orders()

            # excute buy stragegy; shorter waiting time
            is_bought, order = self._execute_buy_order(time_limit=60)
            logger.info('Bought?:%s' %is_bought)
            logger.info('Bought order:%s' %order)

            # excute sell stragegy; longer waiting time
            if is_bought:
                is_sold, order = self._execute_sell_order(order=order,
                                                          time_limit=600)
                logger.info('Sold?:%s' %is_sold)
                logger.info('Sold order:%s' %order)

            # Clean up all the existing order at the end
            self._clean_all_orders()


    def _execute_buy_order(self, pause_time=2, time_limit=600):
        """
        Stragegy for a buying order.
        """
        logger.info('Executing buy order ...... ')

        # parameters
        order = None

        # Get current price
        price = self.army.get_currency_price(self.currency)

        # Get the cloest ema
        ema = self._get_closest_ema(self.granularity, self.num_buckets, 
                                    self.term_n)

        # check if the price is desire to buy.
        # Todo: just simply check price >= ema and decide to buy may be wrong because we don't know if we buy at a very high price (e.gh., the peak), we may have to have a better way to determine if we should excute a buy order. For example, (1) we should determine if the trend of the price is still going up or not (i.e., pass the peak). (2) Or we should let the algorithm to wait from price<=ema to price>=ema, the turning point should be a good price to buy
        logger.info('price:$%s, ema:$%s' %(price,ema))
        if price >= ema:
            order = self.army.buy(price=to_decimal_place(price - 0.1),
                                  size=self.size, 
                                  product_id=self.currency) 

        if order and ('message' not in order) and order['status']!='rejected':
            is_success = self._wait_order_completed(order['id'], pause_time,                                    time_limit)
            return is_success, order
        return False, order


    def _execute_sell_order(self, order, pause_time=2, time_limit=600):
        """
        Stragegy for a selling order. If after the time limit and the LTC is not sold, then check if the current price is high than the buy-in price, if so, sell the LTC at market prize (become a takes that is being charged), else keep the LTC for now (TODO: LTC may accumulate)
        """
        logger.info('Executing sell order ...... ')

        sell_order = self._create_sell_order(order)
        is_sold = self._wait_order_completed(sell_order['id'], pause_time,
                                             time_limit)
        if not is_sold:
            price = self.army.get_currency_price(self.currency)
            
            if price>float(order['price']):
                # cancel original order first and then sell at market price
                self.army.cancel_order(sell_order['id'])

                #new_order = self.army.sell(product_id=self.currency,
                #                       price=price, size=self.size, 
                #                       type='market', post_only=False)
                new_order = None
                logger.info("May sell at market price, I am a taker! Oops")
                return True, new_order
            else:
                return False, sell_order
        return True, sell_order


    def _pass_initial_check(self):
        """
        excute pre-trade check to make sure we are safe to trade
        """
        logger.info('Doing initial check......')

        # manual defined threshold
        value_limit = self.value_limit 
        percent_remain_limit = self.percent_remain_limit 
        size_limit = self.size_limit

        # current acct summary
        acct_summary = self._get_acct_summary()

        # check if the current total value is 10% smaller than the initial value.
        initial_value = self._sum_coin_summary(self.acct_summary)
        current_value = self._sum_coin_summary(acct_summary)
        if (initial_value* percent_remain_limit > current_value):
            return False
        if current_value < value_limit:
            return False 

        # check if the amt coins have too much
        for currency in acct_summary:
            if currency!='USD-USD':
                if acct_summary[currency]['size'] > size_limit:
                    return False

        return True


    def _sum_coin_summary(self, summary):
        """
        Sum all coin values given a summary.

        :params summary: summary of all the coin size and price
        """
        total = 0
        for coin in summary:
            total += summary[coin]['price'] * summary[coin]['size']
        return total


    def _get_acct_summary(self):
        """
        Get summary of acct, such as how many coins, etc
        """
        summary = {}
        accts = self.army.get_accts_dict()
        for currency in accts:
            time.sleep(0.25) #pause x second to avoid api call failure

            currency_type = 'USD'
            size = float(accts[currency]['balance'])

            if currency!='USD':
                price = self.army.get_currency_price(currency+'-USD')
                currency_type = 'coin'
            else:
                price = 1

            summary[currency+'-USD'] = {'size':size, 'price':price,
                                         'currency_type':currency_type
                                        }
        return summary


    def _wait_order_completed(self, id, pause_time=2, time_limit=600):
        """
        Wait an order to be completed within a time limit

        :params pause_time: pausing time(2) before calling the api again
        :params time_limit: maximum time(2) to wait
        """
        while not self._is_order_filled(id=id):
            if (time_limit % 60 == 0):
                logger.info('Order complete remaining time:%s' %time_limit)
                
            time.sleep(pause_time) # pause for x second
            time_limit -= pause_time
            if time_limit <=0:
                return False

        logger.info("Completed order at:%ss" %time_limit)
        return True


    def _create_sell_order(self, buy_order):
        """
        Create a sell order based on info of a buy_order

        :params buy_order: the buy order
        :params gain: the percent gain that is expected to have
        """
        market_price = self.army.get_currency_price(self.currency)
        price = float(buy_order['price'])
        if price>market_price:
            price = (price * (1 + self.sell_gain)) 
        else:
            price = market_price * (1 + self.sell_gain)
        price = to_decimal_place(price)

        order = self.army.sell(price=price, product_id=self.currency, 
                               size=self.size)
        return order


    def _clean_all_orders(self):
        """
        Clean up the orders. 

        Note: if the trading pricinple is a-buy-a-sell, there should be only <=1 existing order.
        """
        logger.info('Cleanning all orders......')

        orders = self.army.get_orders()
        orders = orders[0]

        if orders:
            for order in orders:
                self.army.cancel_order(order['id'])

              
    def _is_order_filled(self, id):
        """
        Check if an order is filled

        :params id: the id of an order
        """
        info = self.army.get_order(id)
        if info['status'] == 'done':
            return True
        else:
            return False


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






	
