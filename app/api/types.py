#coding=utf-8
from validate_email import validate_email
from email.utils import parsedate_tz, mktime_tz
from datetime import datetime

def email(email_str):
    """Return email_str if valid, raise an exception in other case."""
    if validate_email(email_str):
        return email_str
    else:
        raise ValueError('{} is not a valid email'.format(email_str))

def rfc822(rfc822_str):
    """Return datetime_str if valid, raise an exception in other case."""
    date_tuple = parsedate_tz(rfc822_str)
    if date_tuple:
        return datetime.fromtimestamp(mktime_tz(date_tuple))
    else:
        raise ValueError('{} is not a valid rfc822 date'.format(rfc822_str))
