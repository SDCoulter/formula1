"""
Create a database instance to hold the Formula 1 data.
Using sqlite.
"""

import sqlite3, click

# Check if these are needed as we are not creating users/auth.
from flask import current_app, g
from flask.cli import with_appcontext

# Database connection function.
def get_db():
    # Allow multiple functions access to database during the request.
    if 'db' not in g:
        g.db = sqlite3.connect(
        # Point to current app in use - formula1_data.
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# Close connection to database.
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

# Initialize the database.
def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Add CLI command to init db.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data - create new empty table."""
    init_db()
    click.echo('Database Initialized.')
