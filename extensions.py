"""extensions.py"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from flask_migrate import Migrate

db = SQLAlchemy()
loginmanager = LoginManager()
bcrypt = Bcrypt()

migrate = Migrate()

# Redirect unauthorized users to login page
loginmanager.login_view = "auth.login"  # "auth.login" refers to the login route in the auth blueprint
loginmanager.login_message_category = "warning"  # Optional: Flash category for messages