class GDAXRequestAuth(AuthBase):
    """
    Setting up the Authentication process by extending the AuthBase object.
    """
    
    def __init__(self, api_key, secret_key, passphrase):
        """
        These keys are generated in https://public.sandbox.gdax.com/settings/api.
        
        :params api_key: api key
        :params secret_key: secret key
        :params: passphrase: passprase
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
    
    def __call__(self, request):
        """
        Create the request object with content
        """
        
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message.encode('utf-8'), hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest())
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request

    
class Trader():
    """
    Trader object to handle trading.
    """
    
    def __init__(self, api_base, api_key, secret_key, passphrase):
        """
        These keys are generated in https://public.sandbox.gdax.com/settings/api.
        
        :params api_key: api key
        :params secret_key: secret key
        :params: passphrase: passprase
        """
        self.api_base = api_base
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        
        # create the authentication object
        self.auth = GDAXRequestAuth(self.api_key, self.secret_key, self.passphrase)
        
            
    def products(self):
        """
        Obtain the list of products (e.g., BTC) from Gdax.
        """
        response = requests.get(self.api_base + '/products')
        # check for invalid api response
        if response.status_code is not 200:
            raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
        return response.json()
    
    
    def trade(self, product_id, side, size, price,
            type_='limit', time_in_force='GTC', stp='dc',
            cancel_after=None, post_only=None):
        """
        Perform trade option in Gdax.
        
        :params product_id: currency we want to buy, e.g., 'BTC'
        :params side: sell or buy
        :params price: price value
        :params type_: market or limit
        :params time_in_force: they type of the time we want
        :params stp: self-trade prevention type, e.g., 'dc'
        :params cancel_after: time limit for order
        :params post_only: flag specifies that the order should only make liquidity,
                            and will otherwise result in a rejected order.        
        """
        order_data = {
            'product_id': product_id,
            'side': side,
            'size': size,
            'type': type_,
            'stp' : stp
        }

        if type_ == 'limit':
            order_data['price'] = price
            order_data['time_in_force'] = time_in_force
            
            if 'time_in_force' is 'GTT':
                order_data['cancel_after'] = cancel_after 
            if 'time_in_force' not in ['IOC', 'FOK']:
                order_data['post_only'] = post_only        
                
        response = requests.post(self.api_base + '/orders', data=json.dumps(order_data), auth=self.auth)
        print(response.json())
        if response.status_code is not 200:
            raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
        else:    
            # re-confirm the order to make sure it is not "pending"
            response = self.order_status(response.json()['id'])
        
        return response.json()


    def order_status(self, order_id):
        """
        To re-confirm the order that we makes went through.

        :params order_id: the order id that we made.
        """
        order_url = self.api_base + '/orders/' + order_id
        response = requests.get(order_url, auth=self.auth)
        if response.status_code is not 200:
            raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
        return response

