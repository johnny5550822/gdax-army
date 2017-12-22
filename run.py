import logging
from lib import Trader

# Global logging setup
# www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3


def main():
    # account info
    api_key = '097f67c2c1cb3452f33fcdf143361142'
    secret_key = 'qQvU8RjCksVPF6KtuKMFY+bcgeaSeUlRpLvEdV5L4esiZxwWTVIszuCqXiuYbMVIfWl/NmE1zWqwiFT7xLbz3w=='
    passphrase = 'kznsevl3lgvx3dpk995yzxgvi'

    # Trader
    trader = Trader(api_key=api_key,
                    secret_key=secret_key,
                    passphrase=passphrase)
    trader.trade()

if __name__ == '__main__':
    main()
