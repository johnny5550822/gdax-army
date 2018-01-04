from lib.utils import *
from lib import GdaxArmy, BuyStrategier, SellStrategier
import logging


class Trader():
    """
    Trade controller (bot) that handles all the trading algorithm.
    """

    def __init__(self, api_key, secret_key, passphrase,
                 interest_currency=['LTC', 'USD'],
                 size=0.01, currency='LTC-USD',
                 value_limit=470, percent_remain_limit=0.90, size_limit=0.1,
                 granularity=300, num_buckets=200, term_n=60,
                 macd_short_n=12, macd_long_n=26,
                 trade_option_buy=1, trade_option_sell=1
                 ):
        # setup logger
        time_str = str(get_current_time()).replace(' ', '_')
        self.logger = setup_logger(__name__, 'logs/%s_log.log' % time_str)
        self.trade_logger = setup_logger(__name__ + '_trade',
                                         'logs/%s_trade.log' % time_str)

        # logger
        self.logger.info('')
        self.logger.info('---------------New trade---------------')
        self.trade_logger.info('')
        self.trade_logger.info('---------------New trade---------------')

        # api key
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

        # create the trade army
        self.army = GdaxArmy()
        self.interest_currency = interest_currency
        self.army.authenticate(api_key=api_key,
                               secret_key=secret_key, passphrase=passphrase,
                               interest_currency=self.interest_currency,
                               is_sandbox_url=False)

        # Get initial acct summary
        self.acct_summary = self._get_acct_summary()

        # for buy and sell
        self.size = size
        self.currency = currency

        # initial check parameter, for safety purpose
        self.value_limit = value_limit
        self.percent_remain_limit = percent_remain_limit
        self.size_limit = size_limit

        # strategiers
        self.buyStrategier = BuyStrategier(self.army, currency, granularity,
                                           num_buckets, term_n, macd_short_n,
                                           macd_long_n, time_str
                                           )
        self.sellStrategier = SellStrategier(self.army, currency, granularity,
                                             num_buckets, term_n,
                                             macd_short_n, macd_long_n,
                                             time_str)

        # trade options
        self.trade_option_buy = trade_option_buy
        self.trade_option_sell = trade_option_sell
        self.logger.info('Trade Option:buy(%s),sell(%s)' %
                         (self.trade_option_buy, self.trade_option_sell))

        # log the configuration
        self.logger.info("Initial Account Summary:%s" % self.acct_summary)

    def trade(self):
        """
        Trade using exponential moving average (EMA) in a limit fashion. We 
        are assuming doing one trade (cycle) at a time. A cycle is defined as 
        a-buy-a-sell.

        Note: for now, the algorithm will first&end CANCELL all the existing 
        orders, which may cause 'leftover' in digital coin (e.g., LTC).
        """
        self.logger.info('########## Trade ##########')

        # wait until the pattern favor not to buy (so that we can catch the
        # moment when it is good to buy in the loop).
        while self.buyStrategier.should_buy(option=self.trade_option_buy):
            self.logger.info('Waiting price<ema to start trading cycle.')
            time.sleep(60)

        # loop
        while True:
            self.logger.info('Start trading loop......')

            # security check to make sure it is safe to start investment
            try:
                if self._pass_initial_check():
                    # Clean up all the existing order first
                    self._clean_all_orders()

                    # initial parameters
                    is_bought = False
                    is_sold = False

                    # excute buy stragegy
                    while not is_bought:
                        try:
                            time.sleep(30)  # not overwhelming the api
                            is_bought, buy_order = self._execute_buy_order(
                                time_limit=20,
                                trade_option=self.trade_option_buy)
                            if not is_bought:
                                self._clean_an_order(buy_order)
                            self.logger.info('Bought?:%s' % is_bought)
                        except Exception, e:
                            self.logger.info("Exception:%s" % e)
                    self.logger.info('Bought order:%s' % buy_order)
                    self._log_trade(buy_order)

                    # excute sell stragegy
                    while not is_sold:
                        try:
                            time.sleep(30)  # not overwhelming the api
                            is_sold, sell_order = self._execute_sell_order(
                                order=buy_order,
                                time_limit=20,
                                trade_option=self.trade_option_sell)
                            if not is_sold:
                                self._clean_an_order(sell_order)
                            self.logger.info('Sold?:%s' % is_sold)
                        except Exception, e:
                            self.logger.info("Exception:%s" % e)
                    self.logger.info('Sold order:%s' % sell_order)
                    self._log_trade(sell_order)

            except Exception, e:
                self.logger.info("Exception:%s" % e)

    def _clean_all_orders(self):
        """
        Clean up the orders. 

        Note: if the trading pricinple is a-buy-a-sell, there should be only 
        <=1 existing order.
        """
        self.logger.info('Cleanning all orders......')

        orders = self.army.get_orders()
        orders = orders[0]

        if orders:
            for order in orders:
                self.army.cancel_order(order['id'])

    def _clean_an_order(self, order):
        """
        Clean a placed order.
        """
        if order is not None and order['id'] is not None:
            self.logger.info('Cancel a placed order...')
            self.army.cancel_order(order['id'])

    def _determine_order_price(self, pos=0, order_type='bids'):
        """
        Determine the limited order price. To be more specifiy, the order book will be obtained and the pos_th order price will be picked to be the price. This can avoid choosing an arbitrary price delta (differential difference) that is not sure how far it is from the current trade price.

        :params pos: position in the order book
        :params order_type: 'bids' for buy and 'asks' for sell
        """
        order_book = self.army.get_product_order_book(
            product_id=self.currency, level=2)
        return(float(order_book[order_type][pos][0]))

    def _execute_buy_order(self, pause_time=2, time_limit=600,
                           trade_option=1):
        """
        Stragegy for a buying order.

        :params: pause_time: time to wait to call the API again
        :params: time_limit: how much time we wait for the excution
        :params: trade strategy option
        """
        self.logger.info('Executing buy order ...... ')

        # check if should sell.
        if self.buyStrategier.should_buy(option=trade_option):
            price = self._determine_order_price(order_type='bids')
            order = self.army.buy(price=to_decimal_place(price),
                                  size=self.size,
                                  product_id=self.currency)
            self.logger.info('Current price:%s' % (price))

            if self._is_order_placed(order):
                self.logger.info('Placed a buy order.')
                is_bought = self._wait_order_complete(order['id'],
                                                      pause_time, time_limit)
                return is_bought, order
        return False, None

    def _execute_sell_order(self, order, pause_time=2, time_limit=600,
                            trade_option=1):
        """
        Stragegy for a selling order. If after the time limit and the LTC is 
        not sold, then check if the current price is high than the buy-in 
        price, if so, sell the LTC at market prize (become a takes that is 
        being charged), else keep the LTC for now (TODO: LTC may accumulate)

        :order: buy order (which has been executed) info
        :params: pause_time: time to wait to call the API again
        :params: time_limit: how much time we wait for the excution
        :params: trade strategy option
        """
        self.logger.info('Executing sell order ...... ')

        # check if should sell
        if self.sellStrategier.should_sell(buy_order=order,
                                           option=trade_option):
            price = self._determine_order_price(order_type='asks')
            sell_order = self.army.sell(price=to_decimal_place(price),
                                        size=self.size,
                                        product_id=self.currency)
            self.logger.info('Current price:%s' % (price))

            if self._is_order_placed(sell_order):
                self.logger.info('Placed a sell order.')
                is_sold = self._wait_order_complete(sell_order['id'],
                                                    pause_time, time_limit)
                if not is_sold:
                    self.logger.info('Not sell sell order. Consider resell.')
                    self.army.cancel_order(sell_order['id'])
                    if self.sellStrategier.should_resell(sell_order):
                        self.logger.info('Resell.')
                        new_order = self.army.sell(product_id=self.currency,
                                                   price=price,
                                                   size=self.size,
                                                   type='market',
                                                   post_only=False)
                        new_order['price'] = price  # they missed this info
                        self.logger.info("Sell at market price, I am a taker!")
                        return True, new_order
                return is_sold, sell_order
        return False, None

    def _get_acct_summary(self):
        """
        Get summary of acct, such as how many coins, etc
        """
        summary = {}
        accts = self.army.get_accts_dict()
        for currency in accts:
            time.sleep(0.25)  # pause x second to avoid api call failure

            currency_type = 'USD'
            size = float(accts[currency]['balance'])

            if currency != 'USD':
                price = self.army.get_currency_price(currency + '-USD')
                currency_type = 'coin'
            else:
                price = 1

            summary[currency + '-USD'] = {'size': size, 'price': price,
                                          'currency_type': currency_type
                                          }
        return summary

    def _is_order_filled(self, id):
        """
        Check if an order is filled

        :params id: the id of an order
        """
        order = self.army.get_order(id)
        if order['status'] == 'done':
            return True
        else:
            return False

    def _is_order_placed(self, order):
        """
        Check if the order is placed successfully.

        :params order: the order
        """
        return ('message' not in order) and order['status'] != 'rejected'

    def _log_trade(self, order):
        """
        Log a trade record.

        :params order: the order
        """
        self.trade_logger.info('trade_option:buy(%s),sell(%s)\t%s\t%s\t%s\t%s'
                               % (self.trade_option_buy,
                                  self.trade_option_sell,
                                  order['product_id'],
                                  order['side'],
                                  order['price'],
                                  order['size']))

    def _pass_initial_check(self):
        """
        excute pre-trade check to make sure we are safe to trade
        """
        self.logger.info('Doing initial check......')

        # manual defined threshold
        value_limit = self.value_limit
        percent_remain_limit = self.percent_remain_limit
        size_limit = self.size_limit

        # current acct summary
        acct_summary = self._get_acct_summary()

        # check if the current total value is 10% smaller than the initial
        # value.
        initial_value = self._sum_coin_summary(self.acct_summary)
        current_value = self._sum_coin_summary(acct_summary)
        self.logger.info('Current Acct info: %s' % acct_summary)
        self.logger.info('Current total value: %s' % current_value)
        if (initial_value * percent_remain_limit > current_value):
            return False
        if current_value < value_limit:
            return False

        # check if the amt coins have too much
        for currency in acct_summary:
            if currency != 'USD-USD':
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

    def _wait_order_complete(self, id, pause_time=5, time_limit=600):
        """
        Wait an order to be completed within a time limit

        :params pause_time: pausing time(2) before calling the api again
        :params time_limit: maximum time(2) to wait
        """
        while not self._is_order_filled(id=id):
            if (time_limit % 10 == 0):
                self.logger.info(
                    'Order complete remaining time:%s' % time_limit)

            time.sleep(pause_time)  # pause for x second
            time_limit -= pause_time
            if time_limit <= 0:
                return False

        self.logger.info("Completed order at:%ss" % time_limit)
        return True
