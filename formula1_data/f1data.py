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
        # Search db for default table.
        df = moves.search_con_db(2021, 19)
        # Pass this to the page to fill in default values for SY and RN dropdowns.
        pass_data = {'season_year': 2021, 'round_no': 19}
        # TODO: is there a way to improve the handling of pass_data?

        # Check there is data in the database.
        # TODO: create the method to raise an error here.
        if len(df) == 0:
            raise

    # No db data, make API call.
    except Exception as e:
        # If not in db (first visit) - query API and get DF.
        df = moves.con_standings('https://ergast.com/api/f1/current/constructorStandings.json')
        # Store the DataFrame in the database.
        df.to_sql(name='constructor_standings', con=db, if_exists='append')


    # Form sent with data to populate template.
    if request.method == 'POST':
        season_year = request.form['season_year']
        round_no = request.form['round_no']
        # So we can update the default values in the dropdowns on the page.
        pass_data = {'season_year': season_year, 'round_no': round_no}

        # Marker for data being found in the database.
        no_db_data = False
        # Search database instance first for corresponding data.
        try:
            df = moves.search_con_db(season_year, round_no)

            # TODO: create error.
            if len(df) == 0:
                raise

        # Otherwise try to get the data from the API.
        except Exception as e:
            # Find the URL and query the API.
            df = moves.con_standings(moves.parse_con_url(season_year, round_no))
            # Store the newly found data.
            df.to_sql(name='constructor_standings', con=db, if_exists='append')
            # TODO: replace this method, currently doing two searchs for column names.
            df = moves.search_con_db(season_year, round_no)


    # Check if an error was returned during URL parsing.
    if type(df) == 'str':
        flash(df)
        # Send blank DataFrame.
        df = pd.DataFrame()
    else:
        # Only show the columns we need.
        page_df = df[['Position', 'Constructor Name', 'Points', 'Wins']].set_index('Position')
        page_df.index.name = None

    # Pass the data back to the template to display.
    return render_template('f1data/con_standings.html',
                            tables=[page_df.to_html(classes='table')],
                            pass_data=pass_data)

    # Use graphs, etc, to display data depending on request from user. (html/js)
