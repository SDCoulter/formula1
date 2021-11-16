"""
Create a database instance to hold the Formula 1 data.
Using sqlite.
"""

import sqlite3, click

# Check if these are needed as we are not creating users/auth.
from flask import current_app, g
from flask.cli import with_appcontext
