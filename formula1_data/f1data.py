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

    try:
        # Search db for default table.
        df = moves.search_con_db(2021, 20)
        # Pass this to the page to fill in default values for SY and RN dropdowns.
        pass_data = {'season_year': 2021, 'round_no': "20 - Qatar Grand Prix"}

        # Check there is data in the database, otherwise raise an Error.
        if len(df) == 0:
            raise

    # No db data, make API call.
    except Exception as e:
        # If not in db (first visit) - query API and get DF.
        df = moves.con_standings('https://ergast.com/api/f1/current/constructorStandings.json')
        # Store the DataFrame in the database.
        df.to_sql(name='constructor_standings', con=db, if_exists='append')
        # Rename the columns.
        df.columns = moves.pretty_con_names()


    # Form sent with data to populate template.
    if request.method == 'POST':
        season_year = request.form['season_year']
        round_details = request.form['round_no']
        round_no = int(round_details.split(' ')[0])

        # So we can update the default values in the dropdowns on the page.
        pass_data = {'season_year': season_year, 'round_no': round_details}

        # Search database instance first for corresponding data.
        try:
            df = moves.search_con_db(season_year, round_no)

            # Raise an error when no data is found.
            if len(df) == 0:
                raise

        # Otherwise try to get the data from the API.
        except Exception as e:
            # Find the URL and query the API.
            df = moves.con_standings(moves.parse_con_url(season_year, round_no))
            if type(df) != str:
                # Store the newly found data.
                df.to_sql(name='constructor_standings', con=db, if_exists='append')
                # Rename columns.
                df.columns = moves.pretty_con_names()

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
