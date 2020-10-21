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


def time_date():
    """Get current date
    ex: Wednesday, October 14
    """
    """make request to time API"""
    req = requests.get("http://worldtimeapi.org/api/timezone/America/New_York")

    """parse request and extract day and month"""
    dt = parse(req.json()["datetime"])
    day = dt.strftime("%A")
    month = dt.strftime("%B")
    day_n = dt.strftime("%d")
    today = "{}, {} {}".format(day, month, day_n)

    """first day of the week == sunday"""
    cur_date = dt.date()
    day_of_week = req.json()["day_of_week"]
    sunday = ""

    if day_of_week < 7:
        sunday = cur_date - timedelta(days=(day_of_week))
    elif day_of_week == 7:
        sunday = cur_date

    """start and end of current week"""
    s_day = sunday
    s_month = s_day.strftime("%b")
    start_day = s_day.strftime("%d")
    e_day = s_day + timedelta(days=6)
    e_month = e_day.strftime("%b")
    end_day = e_day.strftime("%d")

    s_e_w =  "{} {} - {} {}".format(s_month, start_day, e_month, end_day)

    return (today, sunday, s_e_w)
