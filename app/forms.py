"""APPLICATION FORMS"""
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms import (
    StringField, PasswordField, SelectField,
    SubmitField, FormField, FloatField
)


class Login(FlaskForm):
    """Login Form"""
    email = StringField(
        'email', validators=[DataRequired()],
        render_kw={"placeholder": "Email"})
    password = PasswordField(
        'password', validators=[DataRequired()],
        render_kw={"placeholder": "Password"})
    login_type = SelectField('login type', choices=['company', 'employee'])


class EmployeeRegistration(FlaskForm):
    """Employee Registration Form"""
    first_name = StringField(
        'first_name', validators=[DataRequired()],
        render_kw={"placeholder": "First name"})
    last_name = StringField(
        'last_name', validators=[DataRequired()],
        render_kw={"placeholder": "Last name"})
    email = StringField(
        'email', validators=[DataRequired()],
        render_kw={"placeholder": "Email"})
    password = PasswordField(
        'password', validators=[
            DataRequired(),
            EqualTo('confirm', message='Password must match'), Length(min=8)],
        render_kw={"placeholder": "Password"},)
    confirm = PasswordField('confirm', validators=[
        DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Confirm Password"},)
    login_type = SelectField('login type', choices=['employee', 'company'])
    submit = SubmitField('Sign UP')

    def schema(self):
        """turn abject values into dictionary types"""
        schema = {
            "first_name": self.first_name.data,
            "last_name": self.last_name.data,
            "email": self.email.data,
            "password": self.password.data,
        }
        return schema


class CompanyResgistration(FlaskForm):
    """Employee Registration Form"""
    first_name = StringField(
        'first_name', validators=[DataRequired()],
        render_kw={"placeholder": "First name"})
    last_name = StringField(
        'last_name', validators=[DataRequired()],
        render_kw={"placeholder": "Last name"})
    company_name = StringField(
        'company_name', validators=[DataRequired()],
        render_kw={"placeholder": "Company name"})
    description = StringField(
        'description', validators=[DataRequired()],
        render_kw={"placeholder": "Description"})
    email = StringField(
        'email', validators=[DataRequired()],
        render_kw={"placeholder": "Email"})
    password = PasswordField(
        'password', validators=[
            DataRequired(),
            EqualTo('confirm', message='Password must match'), Length(min=8)],
        render_kw={"placeholder": "Password"},)
    confirm = PasswordField('confirm', validators=[
        DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Confirm Password"},)
    login_type = SelectField('login type', choices=['employee', 'company'])
    submit = SubmitField('Sign UP')

    def schema(self):
        """turn abject values into dictionary types"""
        schema = {
            "first_name": self.first_name.data,
            "last_name": self.last_name.data,
            "email": self.email.data,
            "password": self.password.data,
            "company_name": self.company_name.data,
            "description": self.description.data,
        }
        return schema


class Day():
    """Day subset form for
    days in calendars forms
    """
    hours = 0
    description = ''
    location = ''

    def schema(self):
        """turn object values into dictionary type"""
        schema = {
            "hours": self.hours.data,
            "description": self.description.data,
            "location": self.location.data,
        }

        return schema


class Calendar(FlaskForm):
    """Calendar form"""
    # SUNDAY
    SUN_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    SUN_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    SUN_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})
    #  MONDAY
    MON_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    MON_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    MON_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})
    #  TUESDAY
    TUE_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    TUE_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    TUE_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})
    #  WEDNESDAY
    WED_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    WED_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    WED_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})
    #  THUSDAY
    THU_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    THU_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    THU_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})
    #  FRIDAY
    FRI_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    FRI_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    FRI_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})
    #  SATURDAY
    SAT_HOUR = FloatField(
        'hour',
        render_kw={"placeholder": "0"},
        default=0)
    SAT_LOCAL = StringField('location', render_kw={"placeholder": "location"})
    SAT_DESCRIPTION = StringField(
        'description', render_kw={"placeholder": "description"})

    def schema(self):
        """turn object values into dictionary type"""
        schema = {
            "sunday": {
                "hours": self.SUN_HOUR.data,
                "description": self.SUN_DESCRIPTION.data,
                "location": self.SUN_LOCAL.data,
            },
            "monday": {
                "hours": self.MON_HOUR.data,
                "description": self.MON_DESCRIPTION.data,
                "location": self.MON_LOCAL.data,
            },
            "tuesday": {
                "hours": self.TUE_HOUR.data,
                "description": self.TUE_DESCRIPTION.data,
                "location": self.TUE_LOCAL.data,
            },
            "wednesday": {
                "hours": self.WED_HOUR.data,
                "description": self.WED_DESCRIPTION.data,
                "location": self.WED_LOCAL.data,
            },
            "thursday": {
                "hours": self.THU_HOUR.data,
                "description": self.THU_DESCRIPTION.data,
                "location": self.THU_LOCAL.data,
            },
            "friday": {
                "hours": self.FRI_HOUR.data,
                "description": self.FRI_DESCRIPTION.data,
                "location": self.FRI_LOCAL.data,
            },
            "saturday": {
                "hours": self.SAT_HOUR.data,
                "description": self.SAT_DESCRIPTION.data,
                "location": self.SAT_LOCAL.data,
            },
        }

        return schema


class Password(FlaskForm):
    """Change password field"""
    password = PasswordField(
        'password', validators=[
            DataRequired(),
            EqualTo('confirm', message='Password must match'), Length(min=8)],
        render_kw={"placeholder": "Password"},)
    confirm = PasswordField('confirm', validators=[
        DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Confirm Password"},)
