#!/usr/bin/env python3
"""weekly calendar generator module
"""
import datetime
import json


def start_end_week(start_week):
    """Generate weekly start and end date
    """
    week_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    week = []
    end_week = start_week + datetime.timedelta(days=6)
    for day in range(7):
        today = start_week
        next_day = start_week + datetime.timedelta(days=day)
        week.append("{}|{}".format(week_days[day], str(next_day)))
        today = next_day
    key = "{}__{}".format(start_week, end_week)
    return (key, end_week, week)


class WorkDescription():
    """Work history template
    """

    def __init__(self, hour=0, location="", job_description=""):
        """init class
        """
        self.hour = hour
        self.location = location
        self.job_description = job_description

    def object(self):
        """dictionary repr of
        Work Description
        """
        object = {
            "HOUR": self.hour,
            "LOCATION": self.location,
            "DESCRIPTION": self.job_description
        }
        return object

    def __str__(self):
        """return json repr
        of object
        """
        return json.dumps(self.object(), indent=4)


class WeekCalendar():
    """creating a weekly calendar
    """

    def __init__(self, start_date):
        """init class
        """
        self.employee_id = ""
        self.is_week_over = False
        self.start_date = start_date
        self.week_info = start_end_week(self.start_date)
        self.end_date = self.week_info[1]
        self.week = self.week_info[2]
        self.week_id = self.week_info[0]
        self.SUN = WorkDescription()
        self.MON = WorkDescription()
        self.TUE = WorkDescription()
        self.WED = WorkDescription()
        self.THU = WorkDescription()
        self.FRI = WorkDescription()
        self.SAT = WorkDescription()

    def template(self):
        """weekly template
        """
        template = {
            "employee_id": self.employee_id,
            "is_week_over": self.is_week_over,
            "start_date": str(self.start_date),
            "end_date": str(self.end_date),
            self.week[0]: self.SUN.object(),
            self.week[1]: self.MON.object(),
            self.week[2]: self.TUE.object(),
            self.week[3]: self.WED.object(),
            self.week[4]: self.THU.object(),
            self.week[5]: self.FRI.object(),
            self.week[6]: self.SAT.object()
        }
        return template

    def get_work_description(self, day):
        """get work description
        for given day
        """
        week_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        if day in week_days:
            return eval("self.{}.object()".format(day))
        else:
            return print("day must be the following {}".format(week_days)), -1

    def set_work_description(self, day="", hour=0, location="", descrip=""):
        """set working history
        """
        week_days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
        assign_data = ""
        if day in week_days:
            if type(hour) == int or type(hour) == float:
                assign_data = "self.{}.hour = {}\nself.{}.location = \'{}'\
                    \nself.{}.job_description = '{}'\
                    ".format(day, hour, day, location, day, descrip)
                exec(assign_data)
            else:
                return print("hour needs to be type int"), -1
        else:
            return print("day must be the following {}".format(week_days)), -1

    def object(self):
        """dictionary repr of class
        """
        object = {
            self.week_id: self.template()
        }
        return object

    def __str__(self):
        """string repr of class
        """
        return json.dumps(self.object(), indent=4)
