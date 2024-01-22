import datetime
import pytz

def compute_transaction_time():
    """
    Computes the current transaction time in 'Etc/GMT+5' timezone.

    :rtype: datetime.datetime
    :return: The current date and time in 'Etc/GMT+5' timezone.
    """
    utc_dt = datetime.datetime.now(pytz.timezone("UTC"))
    return utc_dt.astimezone(pytz.timezone('Etc/GMT+5'))