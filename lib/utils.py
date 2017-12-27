"""
Utilities functions to support trading in Gdax.
"""
from datetime import datetime
import tzlocal
import logging
import time
from pytz import timezone, utc


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
    # Set timezone converter
    logging.Formatter.converter = _customTime

    # set formmater
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

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


def _customTime(*args):
    utc_dt = utc.localize(datetime.utcnow())
    my_tz = timezone("America/Los_Angeles")
    converted = utc_dt.astimezone(my_tz)
    return converted.timetuple()


def get_current_time():
    """
    Get current time in PST.
    """
    tz = timezone('America/Los_Angeles')
    ct = datetime.now(tz)
    return ct.strftime('%Y-%m-%d_%H-%M-%S')
