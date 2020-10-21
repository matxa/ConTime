#!/usr/bin/env python3
"""Forms
"""
from wtforms.validators import (
    InputRequired,
    Email,
    Length,
    EqualTo,
    ValidationError,
    DataRequired)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DecimalField


class LoginForm(FlaskForm):
    """class for getting form data
    and validate it
    """
    email = StringField(
        "email",
        render_kw={"placeholder": "Email"},
        validators=[InputRequired()])

    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password"},
        validators=[InputRequired()])


# Registration Form
class RegisterForm(FlaskForm):
    """class for registering a new user
    if user exist or input is not the rigth format
    throw error
    """
    first_name = StringField(
        "first_name",
        render_kw={"placeholder": "First Name"},
        validators=[InputRequired()])\

    last_name = StringField(
        "last_name",
        render_kw={"placeholder": "Last Name"},
        validators=[InputRequired()])

    email = StringField(
        "email",
        render_kw={"placeholder": "Email"},
        validators=[
            DataRequired(message="Enter Email"),
            Email()])

    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password"},
        validators=[
            InputRequired(),
            Length(min=8, max=80),
            EqualTo('confirm_pwd', message='Passwords must match')])

    confirm_pwd = PasswordField(
        'Repeat Password',
        render_kw={"placeholder": "Confirm Password"},
        validators=[])


# Add employees Form
class AddEmployee(FlaskForm):
    """Add employees to api
    """
    first_name = StringField(
        "first_name",
        render_kw={"placeholder": "First Name"},
        validators=[InputRequired()])

    last_name = StringField(
        "last_name",
        render_kw={"placeholder": "Last Name"},
        validators=[InputRequired()])

    email = StringField(
        "email",
        render_kw={"placeholder": "Email"},
        validators=[
            DataRequired(message="Enter Email"),
            Email()])


# Change password
class ChangepwdForm(FlaskForm):
    """Form to change password
    """
    password = PasswordField(
        "password",
        render_kw={"placeholder": "Password"},
        validators=[
            InputRequired(),
            Length(min=8, max=80),
            EqualTo('confirm_pwd', message='Passwords must match')])

    confirm_pwd = PasswordField(
        'Repeat Password',
        render_kw={"placeholder": "Confirm Password"},
        validators=[])


# days of the week input
class DaysOfWeek(FlaskForm):
    """Form to get all the
    days of the week
    """
    sunday = ""
    employee_id = ""
    employer_id = ""
    is_week_over = False
    
    # SUNDAY
    SUN_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    SUN_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    SUN_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})
    #  MONDAY
    MON_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    MON_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    MON_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})
    #  TUESDAY
    TUE_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    TUE_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    TUE_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})
    #  WEDNESDAY
    WED_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    WED_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    WED_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})
    #  THUSDAY
    THU_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    THU_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    THU_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})
    #  FRIDAY
    FRI_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    FRI_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    FRI_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})
    #  SATURDAY
    SAT_HOUR = IntegerField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    SAT_LOCAL = StringField('location', render_kw={"placeholder": "LOCAL"})
    SAT_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "DES"})


    def week(self):
        """Generate calendar for
        db
        """
        """SUNDAY"""
        sun = {
            "SUN_HOUR": self.SUN_HOUR.data,
            "SUN_LOCATION": self.SUN_LOCAL.data,
            "SUN_DESCRIPTION": self.SUN_DESCRIPTION.data
        }
        """MONDAY"""
        mon = {
            "MON_HOUR": self.MON_HOUR.data,
            "MON_LOCATION": self.MON_LOCAL.data,
            "MON_DESCRIPTION": self.MON_DESCRIPTION.data
        }
        """TUESDAY"""
        tue = {
            "TUE_HOUR": self.TUE_HOUR.data,
            "TUE_LOCATION": self.TUE_LOCAL.data,
            "TUE_DESCRIPTION": self.TUE_DESCRIPTION.data
        }
        """WEDNESDAY"""
        wed = {
            "WED_HOUR": self.WED_HOUR.data,
            "WED_LOCATION": self.WED_LOCAL.data,
            "WED_DESCRIPTION": self.WED_DESCRIPTION.data
        }
        """THURSDAY"""
        thu = {
            "THU_HOUR": self.THU_HOUR.data,
            "THU_LOCATION": self.THU_LOCAL.data,
            "THU_DESCRIPTION": self.THU_DESCRIPTION.data
        }
        """FRIDAY"""
        fri = {
            "FRI_HOUR": self.FRI_HOUR.data,
            "FRI_LOCATION": self.FRI_LOCAL.data,
            "FRI_DESCRIPTION": self.FRI_DESCRIPTION.data
        }
        """SATDAY"""
        sat = {
            "SAT_HOUR": self.SAT_HOUR.data,
            "SAT_LOCATION": self.SAT_LOCAL.data,
            "SAT_DESCRIPTION": self.SAT_DESCRIPTION.data
        }

        return [sun, mon, tue, wed, thu, fri, sat]

    def week_id(self):
        """week id
        """
        wi = "{}|{}|{}".format(self.sunday, self.employee_id, self.employer_id)
        return wi

    def total_hours(self):
        """get weeks total hour
        """
        total = self.SUN_HOUR.data + self.MON_HOUR.data + self.TUE_HOUR.data +\
            self.WED_HOUR.data + self.THU_HOUR.data + self.FRI_HOUR.data +\
            self.SAT_HOUR.data
        
        return str(total)

    def object(self):
        """Dump into DB
        """

        object = {
            "week_id": self.week_id(),
            "employee_id": self.employee_id,
            "employer_id": self.employer_id,
            "is_week_over": self.is_week_over,
            "total_hours": total_hours(),
            "week": self.week()
        }

        return object
