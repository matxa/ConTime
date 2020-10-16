#!/usr/bin/env python3
"""Where all the utility functions live
helper functions
"""
from datetime import date
import hashlib


def hash_pwd(password):
    """function to hash
    user's password
    """
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_pwd(password, hash):
    """check if password
    and hash match
    """
    if hash_pwd(password) == hash:
        return True
    return False


def today_date():
    """Get current date
    ex: Wednesday, October 14
    """
    dt = date.today()
    day = dt.strftime("%A")
    month = dt.strftime("%B")
    day_n = dt.strftime("%d")
    return "{}, {} {}".format(day, month, day_n)


def strip_date(date):
    """strip date from string
    """
    day = date.strftime("%A")
    month = date.strftime("%B")
    day_n = date.strftime("%d")
    return "{}, {} {}".format(day, month, day_n)
