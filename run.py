import logging
from lib import Trader

# Global logging setup
# www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3
logging.basicConfig(filename="logs/log.log",
                    level=logging.INFO,
                    format="%(asctime)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def main():
    # account info
    api_key = '872d7f979e967e98e8fecdf3c4fc317e'
    secret_key = 'FR+1V4Y8hbzHW8IeoPXybxa6AMpYRJm1OuRbA7EaG0OepQq77c/Ol+tFH7FpC/ch6AiGBwxFzImiGRGdbQYszQ=='
    passphrase = 'do3045sam5qtjne0dw2pdgqfr'

    # Trader
    trader = Trader(api_key=api_key,
                    secret_key=secret_key,
                    passphrase=passphrase)
    trader.trade()

if __name__ == '__main__':
    main()
