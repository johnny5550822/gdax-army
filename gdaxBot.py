"""
Bot that performs a one to one transactions.
"""

from utils import *

class bot():
    """
    An object that uses the util API to perform simple transactions on the gdax platfform.
    """
    
    def __init__(self, api_key, secret_key, passphrase, is_sandbox_url):
        
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.is_sandbox_url = is_sandbox_url
        self.authenticate = False
        
        self.buying_status = False
        self.selling_status = False
        self.currency = 'LTC-USD'
        self.size = 0.01
        self.current_price = None
        self.buying_price = None
        self.selling_price = None
        self.percentage_price = None
        self.highest_price = None
        self.lowest_price = None
        self.profit = None
        
        self.army = None
        
    def __call__(self,authenticate):
        """
        Create a Gdax army object.
        """        
        self.authenticate = authenticate
        
        if authenticate:
            army = GdaxArmy()
            army.authenticate(api_key = self.api_key, secret_key = self.secret_key,
                              passphrase = self.passphrase, is_sandbox_url = self.is_sandbox_url)
            print("Army created, Ready to deploy bots!")
        else:
            army = GdaxArmy()
            print("Army created, No authentication, cannot deploy bots!")
            
        self.army = army
                
           
    def deployBot(self, num_transaction_pairs, percentage_price):
        """
        Demploying a bot. Rules or models of trading must be defined here.
        """

        
        self.percentage_price = percentage_price
        
        print('Bot deployed ...')
        
        ############################
        #buy and sell rules will go here
        # calculate profit and add
        
        profit = self.trade()
        
        ############################
        
        print('Finished transaction pair with ', profit,'profit')
        
    def simple_trading_rule(self):
        self.current_price = self.army.get_currency_price(currency=self.currency)
        print('Current price',self.current_price)

        ## buy
        self.buying_trade()

        ## sell
        self.selling_trade()

        #### reporting profit
        self.profit = self.profit_report()

        return self.profit    
        
    def trade(self):
        self.current_price = self.army.get_currency_price(currency=self.currency)
        
        ## buy
        self.buying_trade()
        
        #initialize lowest and highest prices
        self.lowest_price = self.current_price
        self.highest_price = self.current_price
        
        #### percentage price
        self.percentage_price = self.percentage_price/self.current_price
        
        profit = 0

        ############################
        for i in range(50):
            
            self.update_lowest_price()
                
            self.update_highest_price()
                
            self.current_price = self.army.get_currency_price(currency=self.currency)
            
            if self.current_price <= self.highest_price*(1+self.percentage_price) and self.selling_status==True:
                ## buy
                self.buying_trade()
                self.selling_status=False
            elif self.current_price >= self.lowest_price*(1-self.percentage_price) and self.buying_status==True:
                ## sell
                self.selling_trade()
                self.buying_status=False
                
                #### reporting profit
                profit += self.profit_report()
                
            print(self.percentage_price)
            
        
        return profit
    
    def buying_trade(self):
        """
            A Buying transaction.
        """
        ## buy
        self.army.buy(price=self.current_price, size=self.size, product_id=self.currency, post_only=True)
        self.buying_price = self.current_price
        self.buying_status = True
        print('Buying price',self.current_price)
        
    def selling_trade(self):
        """
            A Buying transaction.
        """
        ## sell
        self.army.sell(price=self.current_price, size=0.01, product_id='LTC-USD', post_only=True)
        self.selling_price = self.current_price
        self.selling_status = True
        print('Selling price',self.current_price)
        
    def profit_report(self):
        """
            Profits from a pair of buying and selling transaction.
        """
        return self.selling_price - self.buying_price
    
    def update_lowest_price(self):
        """
            Updating the lowest price over time.
        """
        if self.current_price <= self.lowest_price:
            self.lowest_price = self.current_price
            
    def update_highest_price(self):
        """
            Updating the highest price over time.
        """
        if self.current_price >= self.highest_price:
            self.highest_price = self.current_price