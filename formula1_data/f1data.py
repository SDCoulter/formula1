"""
Create the Blueprints to allow us to start displaying data.
"""

import pandas as pd
# Check which modules to import.
from flask import (
    Blueprint, render_template, request, flash
)

from formula1_data.db import get_db
# Import the function to request and parse constructor standings data from API.
from . import f1data_query

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
    # Connect to database.
    db = get_db()
    # Get df and pass data returned.
    df, pass_data = f1data_query.get_con_df(db, 2021, "20 - Qatar Grand Prix", first=True)

    # If user chooses new data to find.
    if request.method == 'POST':
        season_year = request.form['season_year']
        round_details = request.form['round_no']

        df, pass_data = f1data_query.get_con_df(db, season_year, round_details)

    # Check if an error was returned during URL parsing.
    if type(df) == str:
        # Flash error on page and send blank DataFrame.
        flash(df)
        page_df = pd.DataFrame()
    else:
        # Only show the columns we need.
        page_df = df[['Position', 'Constructor Name', 'Points', 'Wins']].set_index('Position')
        page_df.columns.name = 'Position'
        page_df.index.name = None

    # Pass the data back to the template to display.
    return render_template('f1data/con_standings.html',
                            tables=[page_df.to_html(classes='table')],
                            pass_data=pass_data)
