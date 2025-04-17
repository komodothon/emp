"""app/services/role_decorator.py"""

from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please login to access this page.", "warning")
                return redirect(url_for("auth.login"))
            
            if current_user.role and current_user.role.name in roles:
                return func(*args, **kwargs)
            
            flash("You are not authorised to access this page.", "danger")
            return redirect(url_for("main.dashboard"))
        return wrapper
    return decorator