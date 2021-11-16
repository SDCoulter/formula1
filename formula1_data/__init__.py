"""
Init file for the Formula 1 Data Analysis application.
"""

# Dependencies.
import os
from flask import Flask

# Factory function.
def create_app(test_config=None):
    # Flask instance.
    app = Flask(__name__, instance_relative_config=True)

    # Defaults.
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Database to hold F1 data.
        DATABASE=os.path.join(app.instance_path, 'formula1_data.sqlite')
    )

    # Check if we are testing the application.
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Check instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Create test route.
    @app.route('/app_func')
    def app_func():
        return 'The application is functioning.'

    # Register the database with the application.
    from . import db
    db.init_app(app)

    # Return the app.
    return app
