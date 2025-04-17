"""run.py"""

import os

from dotenv import load_dotenv
from app import create_app

# Load environment variables
load_dotenv() 

env = os.environ.get("FLASK_ENV", "production").lower()

if env == "development":
    config_class = "config.DevConfig"
elif env == "testing":
    config_class = "config.Testconfig"
else:
    config_class = "config.ProdConfig"



# This line is needed in this place outside 'main' for Gunicorn while deploying
app = create_app(config_class=config_class)

def main():
    app.run(host="0.0.0.0", port=5000, debug=app.config.get("DEBUG", False))


if __name__ == "__main__":
    main()