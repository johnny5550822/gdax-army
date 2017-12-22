import logging
from lib import Trader

# Global logging setup
# www.digitalocean.com/community/tutorials/how-to-use-logging-in-python-3

def main():
    # account info
    api_key = '4247ce199cba7a154cf4013de1e4cd6c'
    secret_key = 'YAJGFXxT/5YSqK5cf1ny52rEEoEXv+PeNcgcBXf2tDI7DHBpNH2t02bbKn1wVRf/SmqJ0nOnHx+KkvjOcpaY/w=='
    passphrase = '4nqonu889hdzi86kydgou323xr'

    # Trader
    trader = Trader(api_key=api_key,
                    secret_key=secret_key,
                    passphrase=passphrase)
    trader.trade()

if __name__ == '__main__':
    main()
