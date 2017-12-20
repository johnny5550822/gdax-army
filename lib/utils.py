"""
Utilities functions to support trading in Gdax.
"""
from datetime import datetime
import tzlocal

def unix_timestamp_to_readable(timestamp):
    """
    Convert a unix timestamp is readable format

    params timestamp: unix timestamp
    """
    local_timezone = tzlocal.get_localzone() # get pytz timezone
    local_time = datetime.fromtimestamp(timestamp, local_timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S.%f%z (%Z)")    


def to_decimal_place(x, decimal_place=2):
    """
    Correct the number to some decimal place
    """
    decimal = '{0:.%sf}' %decimal_place
    return float(decimal.format(x))








