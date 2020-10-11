#!/usr/bin/env python3
"""ALL API ERROR"""

api_error = {
    "EMAIL_IN_USE": {"error": "email already in use"},
    "MISSING_PARAMS": {"error": "missing params to initialize user"},
    "INVALID_JSON": {"error": "invalid JSON"},
    "INVALID_BOSS_ID": {"error": "Invalid Employer User ID"},
    "INVALID_WORKER": {"error": "employee doesn't exist"},
    "WORK_ALREADY": '{"error": "employee {} is already working for {}"\
        .format(em["email"], employer["email"])}',
    "EXCEPT_ERR": '{"error": str(e)}',
}
