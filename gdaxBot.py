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
        self.current_price = None
        self.buying_price = None
        self.selling_price = None
        self.percentage_price = None
        self.highest_price = None
        self.lowest_price = None
        self.profit = None

        
    def __call__(self, authenticate=self.authenticate):
        """
        Create a Gdax army object.
        """        
        
        if authenticate:
            army = GdaxArmy().authenticate(api_key = self.api_key, secret_key = self.secret_key,
                                           passphrase = self.passphrase, is_sandbox_url = self.is_sandbox_url)
        else:
            army = GdaxArmy()
        
        self.current_price = army.get_currency_price(currency=self.currency)
        
        return army
    
    def deployBot(self, num_transaction_pairs, percentage_price, army):
        self.percentage_price = percentage_price
        
        print('Bot deployed ...')
        print('Buying @ X price')
        ############################
        #buy and sell rules will go here
        # calculate profit and add
        
        ############################
        
        print('Finished transaction pari with X profit')
        
        
    
    