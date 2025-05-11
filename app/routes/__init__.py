"""app/routes/__init__.py"""

from flask import Blueprint

# Import Blueprints from routes
from .admin import admin_bp
from .auth import auth_bp
from .main import main_bp
from .departments import departments_bp
from .test import test_bp
from .payroll_route import payroll_bp

all_blueprints = [
    admin_bp,
    auth_bp,
    main_bp,
    departments_bp,
    test_bp,
    payroll_bp,
]