"""
Utilities functions to support trading in Gdax.
"""
from datetime import datetime
import tzlocal
import logging
import time

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')


def unix_timestamp_to_readable(timestamp):
    """
    Convert a unix timestamp is readable format

    params timestamp: unix timestamp
    """
    local_timezone = tzlocal.get_localzone()  # get pytz timezone
    local_time = datetime.fromtimestamp(timestamp, local_timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)")


def to_decimal_place(x, decimal_place=2):
    """
    Correct the number to some decimal place

    :params decimal_Place: decimal place I want to pick
    """
    decimal = '{0:.%sf}' % decimal_place
    return float(decimal.format(x))


def setup_logger(name, log_file, level=logging.INFO):
    """
    Function setup as many loggers as you want

    :params log_file: log file location
    :params level: logging level
    """

    # set FileHandler
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    # set StreamHandler so that you can see in terminal
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    return logger

def get_current_time():
    """
    Get current time.
    """
    return time.asctime(time.localtime(time.time()))
