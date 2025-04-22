"""app/__init__.py"""

import os


from flask import Flask
from extensions import db, loginmanager, bcrypt, migrate
from dotenv import load_dotenv

load_dotenv()


def create_app(config_class="config.DevConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    loginmanager.init_app(app)
    bcrypt.init_app(app)

    migrate.init_app(app, db)

    # Import your models BEFORE create_all()
    from app.models import User, UserCredential, Department, Role, Designation, ContractType, Status

    # Create tables only for dev config
    if os.getenv("FLASK_ENV") == "development":
        print(f'[app/__init__.py] FLASK_ENV: {os.getenv("FLASK_ENV")}')

        # with app.app_context():
        #         db.create_all()
        #         print("[INFO] Tables created (FLASK_ENV=development)")

    # Register blueprints
    from app.routes import all_blueprints
    for blueprint in all_blueprints:
        app.register_blueprint(blueprint)
    

    return app

