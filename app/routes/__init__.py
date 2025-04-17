"""app/routes/__init__.py"""

from flask import Blueprint

# Import Blueprints from routes
from .admin import admin_bp
from .auth import auth_bp
from .main import main_bp

all_blueprints = [
    admin_bp,
    auth_bp,
    main_bp,
]