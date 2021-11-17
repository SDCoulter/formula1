"""
Create the Blueprints to allow us to start displaying data.
"""

import pandas as pd
# Check which modules to import.
from flask import (
    Blueprint, render_template, request
)

from formula1_data.db import get_db
# Import the function to request and parse constructor standings data from API.
from . import moves

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
    db = get_db()

    # TODO: create default behaviour so data can be passed to the page before user selection.
    # TODO: make the values chosen automated to the latest.
    # for now we will just use season 2021 and round 19.
    try:
        # Search database for default dataframe.
        df = db.execute(
            'SELECT * FROM constructor_standings'
            ' WHERE season_year = ? AND round_no = ?',
            (2021, 19)
        ).fetchall()
    except:
        # If not in db (first visit) - query API and get DF.
        df = moves.con_standings('https://ergast.com/api/f1/current/constructorStandings.json')

    # Form sent with data to populate template.
    if request.method == 'POST':
        season_year = request.form['season_year']
        round_no = request.form['round_no']

        # Marker for data being found in the database.
        no_db_data = False
        # Search database instance first for corresponding data.
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
            data_match = pd.DataFrame()
            # TODO: parse the selection to create the url.
            # TODO: use the moves.py function to collect the data and return a DataFrame
            # TODO: store the data in the db.


    # Check if an error was returned during URL parsing.
    if type(df) == 'str':
        flash(df)
        # Send blank DataFrame.
        df = pd.DataFrame()
    else:
        # Only show the columns we need.
        page_df = df[['Position', 'Constructor Name', 'Points', 'Wins']].set_index('Position')

    # Pass the data back to the template to display.
    return render_template('f1data/con_standings.html', tables=[page_df.to_html(classes='data')])

    # Use graphs, etc, to display data depending on request from user. (html/js)
