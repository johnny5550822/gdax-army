"""
Utilities functions to support trading in Gdax.
"""

from requests.auth import AuthBase
import base64, hashlib, hmac, time, json, requests

from datetime import datetime
import tzlocal
import gdax
import pandas as pd

def _unix_timestamp_to_readable(timestamp):
    """
    Convert a unix timestamp is readable format

    params timestamp: unix timestamp
    """
    local_timezone = tzlocal.get_localzone() # get pytz timezone
    local_time = datetime.fromtimestamp(timestamp, local_timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)")    


class GdaxArmy():
    """
    An API object that is built on top of unofficial Gdax python api:
    https://github.com/danpaquin/gdax-python
    """

    def __init__(self):
        self.client = gdax.PublicClient()
        self.auth_client = None


    def authenticate(self, api_key, secret_key, passphrase, 
                    is_sandbox_url=True):
        """
        Authenticate the account.
        """
        if is_sandbox_url:
            api_url = 'https://api-public.sandbox.gdax.com'
        else:
            api_url = 'https://api.gdax.com'
        self.auth_client = gdax.AuthenticatedClient(api_key, 
                                                    secret_key, 
                                                    passphrase,
                                                    api_url=api_url
                                                    )

        # Get the acounts info
        accts = self.auth_client.get_accounts()
        self.auth_client.accts_dict = {}
        for acct in accts:
            self.auth_client.accts_dict[acct['currency']]=acct


    def get_accts_dict(self):
        """
        Return the acct in Gdax info.
        """
        return self.auth_client.accts_dict


    def buy(self, price=1, size=0.01, product_id='LTC-USD', 
            post_only=True, **kwargs):
        """
        Perform a buy order. For example buy 0.01 LTC @100 USD
        """
        order=self.auth_client.buy(price=price, size=size, 
                                    product_id=product_id,
                                    post_only=True, **kwargs)
        return order
                          

    def sell(self, price=10000, size=0.01, product_id='LTC-USD', 
             post_only=True, **kwargs):
        """
        Perform a sell order. For example sell 0.01 LTC @ 100USD
        """
        order=self.auth_client.sell(price=price, size=size, 
                                    product_id=product_id, 
                                    post_only=True, **kwargs)
        return order
       

    def get_trade_trends(self, currency='LTC-USD', granularity=3600, 
                        num_buckets=200
                        ):
        """
        Getting the trade trends in a period of time. A period contains num_buckets of buckets. For example, a period can be 24 hours (defined by granularity); this also indicates there will be num_buckets=24 and each bucket has a time interval of an hour. Each bucket contains several information:

        low: lowest price during the bucket interval
        high: highest price during the bucket interval
        open: first trade in the bucket interval
        close: last trade in the bucket interval
        volume: volume of trading activity during the bucket interval

        :params currency: currency that we are interested in
        :params granularity: unit is second. Amt of time in a bucket
        :params num_buckets: number of buckets
        """
        trades = self.client.get_product_historic_rates(currency, 
                                                    granularity=granularity)
        trades = trades[:num_buckets]
        trades = trades[::-1] # closest time goes last
        df = pd.DataFrame(data=trades)

        # convert time to readable
        df[0] = df[0].apply(_unix_timestamp_to_readable)
        
        # assign
        time_, low_, high_, open_, close_, volume_ = df[0], df[1], df[2], \
                                                        df[3], df[4], df[5]
        mean_ = (low_ + high_)/2
        return time_, low_, high_, mean_, open_, close_, volume_


    def get_simple_moving_average(self, df, n=10):
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


    def get_exponential_moving_average(self, df, n=10):
        """
        return the n-day exponential moving average

        :params df: dataframe or series with one column
        :params n: the size of the moving window (number or periods
                        involved)
                        10-20 short-term trends
                        50 mid-term trends
                        200 long-term trends        
        """
        return df.ewm(span=n).mean()


#    def get_currency_price(self, currency='LTC-USD'):
#        """
#        Return the current price of a currency.
#
#        :params currency: the currency for exchange
#        """
#        info = self.client.get_product_order_book(currency, level=1)
#        return float(info['asks'][0][0])

    def get_currency_price(self, currency='LTC-USD'):
        """
        Snapshot information about the last trade (trade id and price), best bid/ask and 24h volume.
        
        Return the current price of a currency.
        
        :params currncy: the currency for exchange
        """
        
        info = self.client.get_product_ticker(product_id=currency)
        return float(info['price'])
    
    

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










