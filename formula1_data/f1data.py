"""
Create the Blueprints to allow us to start displaying data.
"""

# Check which modules to import.
from flask import (
    Blueprint, render_template, request
)

from formula1_data.db import get_db

bp = Blueprint('f1data', __name__)

# Create index route.
@bp.route('/')
def index():
    # Connect to database and get list of data analyses created.
    db = get_db()
    exps = db.execute("SELECT * FROM data_exps ORDER BY id").fetchall()

    return render_template('f1data/index.html', exps=exps)


# Route for constructor standings.
@bp.route('/con_standings', methods=('GET', 'POST'))
def con_standings():

    # TODO: create default so data can be passed to the page before user selection.
    # TODO: bring db creation here for default search.
    data_match = ''

    # Form sent with data to populate template.
    if request.method == 'POST':
        season_year = request.form['season_year']
        round_no = request.form['round_no']

    # Search database instance first for corresponding data.
        db = get_db()
        no_db_data = False

        try:
            data_match = db.execute(
                "SELECT * FROM constructor_standings"
                " WHERE season_year = ? AND round_no = ?"
                " ORDER BY position"
            ).fetchall()
        except:
            no_db_data = True

        # Else find the data from the API.
        if no_db_data:
            data_match = ''
            # TODO: parse the selection to create the url.
            # TODO: use the moves.py function to collect the data and return a DataFrame
            # TODO: store the data in the db.



    # Pass the data back to the template to display.
    return render_template('f1data/con_standings.html', data=data_match)

    # Use graphs, etc, to display data depending on request from user. (html/js)
