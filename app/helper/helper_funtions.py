""" below should be the functions that will be used mostly in any db """
from datetime import datetime as dateconverterdatetime


def convert_dateformat(date):
    """ dateconversion """
    return dateconverterdatetime.strptime(date, '%Y-%m-%d')
