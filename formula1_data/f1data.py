"""
Create the Blueprints to allow us to start displaying data.
"""

# Check which modules to import.
from flask import (
    Blueprint, redirect, render_template
)

from flaskr.db import get_db

bp = Blueprint('f1data', __name__)

# Create index route.
@bp.route('/')
def index():

    """
    Confirm need for db.
    Return index for now.

    db = get_db()
    tables = db.execute(
        "SELECT name FROM sqlite_schema"
        " WHERE type='table'"
        " ORDER BY name"
    ).fetchall()
    """

    return render_template('f1data/index.html')#, tables=tables)
