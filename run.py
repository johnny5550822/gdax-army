import logging
from TradeController import TradeController

# Global logging setup
# https://www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
logging.basicConfig(filename="log.log", 
                    level=logging.INFO,
                    format="%(asctime)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def main():
    # account info
    api_key=''
    secret_key=''
    passphrase=''
    tradeController = TradeController(api_key=api_key,
                                      secret_key=secret_key, 
                                      passphrase=passphrase)
    tradeController.trade_by_ema_limit()

if __name__ == '__main__':
    main()

