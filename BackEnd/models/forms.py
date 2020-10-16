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
from wtforms import StringField, PasswordField


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
