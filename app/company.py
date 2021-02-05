"""COMPANY BLUEPRINT"""
from flask import Blueprint, redirect, url_for, abort
from flask_login import login_required, current_user
from utils import check_user_type

company = Blueprint('company', __name__)


@company.route('/', strict_slashes=False)
@login_required
def dashboard():
    """Check is current user is of type company"""
    if check_user_type(current_user.id) != 'company':
        abort(401)
    return "Company"
