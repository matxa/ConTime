#!/usr/bin/env python3
"""Where all the utility functions live
helper functions
"""
import requests
from datetime import date, timedelta
from dateutil.parser import parse
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
    req = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")
    dt = parse(req.json()["datetime"])
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


def sunday():
    """get the the first day
    of every week
    """
    req = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")
    cur_date = parse(req.json()["datetime"]).date()
    day_of_week = req.json()["day_of_week"]
    sunday = ""

    if day_of_week < 7:
        sunday = cur_date - timedelta(days=(day_of_week))
    elif day_of_week == 7:
        sunday = cur_date

    return (str(sunday), sunday)

def week_start_end():
    """Get current week
    start and end day
    """
    s_day = sunday()[1]
    s_month = s_day.strftime("%b")
    start_day = s_day.strftime("%d")
    e_day = s_day + timedelta(days=6)
    e_month = e_day.strftime("%b")
    end_day = e_day.strftime("%d")

    return "{} {} - {} {}".format(s_month, start_day, e_month, end_day)
