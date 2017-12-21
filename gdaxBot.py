"""
Bot that performs a one to one transactions.
"""

import utils, time

class bot():
    """
    An object that uses the util API to perform simple transactions on the gdax platfform.
    """
    
    def _init_(self, api_base, api_key, secret_key, passphrase, is_sandbox_url, authenticate):
        
        self.api_base = api_base
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.is_sandbox_url = is_sandbox_url
        self.authenticate = authenticate
        
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

        
    def __call__(self, authenticate=self.authenticate):
        """
        Create a Gdax army object.
        """        
        
        if authenticate:
            army = GdaxArmy().authenticate(api_key = self.api_key, secret_key = self.secret_key,
                                           passphrase = self.passphrase, is_sandbox_url = self.is_sandbox_url)
            print("Army created, Ready to deploy bots!")
        else:
            army = GdaxArmy()
            print("Army created, No authentication, cannot deploy bots!")
            
        self.army = army
                
           
    def deployBot(self, num_transaction_pairs, percentage_price):
        
        self.percentage_price = percentage_price
        
        print('Bot deployed ...')
        print('Buying @ X price')
        
        ############################
        #buy and sell rules will go here
        # calculate profit and add
        
        self.profit = trade()
        
        ############################
        
        print('Finished transaction pari with X profit')
        
    def trade():
        self.current_price = self.army.get_currency_price(currency=self.currency)
        
        ## buy
        self.army.buy(price=self.current_price, size=self.size, product_id=self.currency, post_only=True)
        self.buying_status = True
        self.buying_price = self.current_price
        
        #initialize lowest and highest prices
        self.lowest_price = self.current_price
        self.highest_price = self.current_price
        
        ############################
        while !self.selling_status:
            if self.current_price <= self.lowest_price:
                self.lowest_price = self.current_price
                
            if self.current_price >= self.highest_price:
                self.highest_price = self.current_price
                
            self.current_price = self.army.get_currency_price(currency=self.currency)
            
            if self.current_price <= self.highest_price*(1-self.percentage_price) and self.selling_status==True:
                self.army.buy(price=self.current_price, size=0.01, product_id='LTC-USD', post_only=True)
                self.buying_status = True
            elif self.current_price >= self.lowest_price*(1+self.percentage_price):
                self.army.sell(price=self.current_price, size=0.01, product_id='LTC-USD', post_only=True)
                self.selling_price = self.current_price
                self.selling_status = True
        
        profit = self.selling_price - self.buying_price
        
        return profit
    
    