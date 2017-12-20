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
    api_key='00fc1f49830d7ad2d946c3199eb7cfc4'
    secret_key='d5VrZobp9JmtdKGzDXgOEeOt2LMLCPpiG/COCk4tDnDIBJHGt6fvshsfP2wNiaWXi5e2r+A5ut6dqdi0FYScGg=='
    passphrase='7vy5jsfl8mozsro2h08wjexw29'
    tradeController = TradeController(api_key=api_key,
                                      secret_key=secret_key, 
                                      passphrase=passphrase)
    tradeController.trade_by_ema_limit()

if __name__ == '__main__':
    main()

