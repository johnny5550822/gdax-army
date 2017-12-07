"""
Utilities functions to support trading in Gdax.
"""

from requests.auth import AuthBase
import base64, hashlib, hmac, time, json, requests


def products(api_base='https://api-public.sandbox.gdax.com'):
    """
    Obtain the list of products (e.g., BTC) from Gdax.
    
    :params api_base: the base of the api, either the sandbox or the official one.
    """
    response = requests.get(api_base + '/products')
    # check for invalid api response
    if response.status_code is not 200:
        raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
    return response.json()


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

    
def buy_market(product_id, side, size):
    auth = GDAXRequestAuth(api_key, api_secret, passphrase)
    order_data = {
        'type': 'market',
        'side': side,
        'product_id': product_id,
        'size': size
    }
    response = requests.post(api_base + '/orders', data=json.dumps(order_data), auth=auth)
    if response.status_code is not 200:
        raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
    return response.json()


def buy_limit(product_id, price, side, size, time_in_force='GTC', cancel_after=None, post_only=None):
    auth = GDAXRequestAuth(api_key, api_secret, passphrase)
    order_data = {
        'type': 'limit',
        'side': side,
        'product_id': product_id,
        'price': price,
        'size': size,
        'time_in_force': time_in_force
    }
    if 'time_in_force' is 'GTT':
        order_data['cancel_after'] = cancel_after 
    if 'time_in_force' not in ['IOC', 'FOK']:
        order_data['post_only'] = post_only
    response = requests.post(api_base + '/orders', data=json.dumps(order_data), auth=auth)
    if response.status_code is not 200:
        raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
    return response.json()


def order_status(order_id):
    """
    To re-confirm the order that we makes went through.
    
    :params order_id: the order id that we made.
    """
    order_url = api_base + '/orders/' + order_id
    response = requests.get(order_url, auth=auth)
    if response.status_code is not 200:
        raise Exception('Invalid GDAX Status Code: %d' % response.status_code)
    return response.json()










