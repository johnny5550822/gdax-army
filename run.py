import logging
from lib import Trader

# Global logging setup
# www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3

def main():
    # account info
    api_key = ''
    secret_key = ''
    passphrase = ''

    # Trader
    trader = Trader(api_key=api_key,
                    secret_key=secret_key,
                    passphrase=passphrase)
    trader.trade()

if __name__ == '__main__':
    main()
