"""
Create a database instance to hold the Formula 1 data.
Using sqlite.
"""

import sqlite3, click

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
        # Import the table information to initialize in the database.
        from . import db_table_data
        db.executemany(
            'INSERT INTO data_exps (id, name, url, description, date_created, function_name, function_url)'
            ' VALUES (?, ?, ?, ?, ?, ?, ?)',
            db_table_data.table_list
        )
        # Commit these changes to the database.
        db.commit()

# Add CLI command to init db.
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data - create new empty table."""
    init_db()
    click.echo('Database Initialized.')

# Function to register the application.
def init_app(app):
    # Call function when cleaning up after return response.
    app.teardown_appcontext(close_db)
    # Add new flask command line command.
    app.cli.add_command(init_db_command)
