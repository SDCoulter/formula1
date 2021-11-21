"""
A place to store the functions to be used to call data from API.
"""

import pandas as pd
import requests
from formula1_data.db import get_db


def p_z(value):
    """ Return string value with preceding 0 if value is length 1. """
    s_val = str(value)
    return f"0{s_val}" if len(s_val) == 1 else s_val


def parse_con_standings(data):
    """
    Data returned from the request is parsed into more usable formats.
    Returns name and DataFrame.
    """
    try:
        # Separate the data.
        season_year = data['season']
        round_no = data['round']
        constructor_standings = data['ConstructorStandings']

        # Manipulate the data to a neater DataFrame.
        df = pd.DataFrame(constructor_standings)
        df['Constructor Name'] = df['Constructor'].apply(lambda value: value['name'])
        df['Constructor URL'] = df['Constructor'].apply(lambda value: value['url'])
        df['Constructor Nationality'] = df['Constructor'].apply(lambda value: value['nationality'])
        df['Season'] = season_year
        df['Round'] = round_no

        # Create unique identifier.
        df['uid'] = df['position'].apply(lambda value: str(season_year) + p_z(round_no) + p_z(value))

        df = df.set_index('uid').drop(columns=['positionText', 'Constructor'])
        # Convert columns to names stored in the SQLite db.
        df.columns = ['position', 'points', 'wins', 'constructor_name', 'constructor_url',
                          'constructor_nationality', 'season_year', 'round_number']
        df = df[['position', 'constructor_name', 'points', 'wins', 'constructor_url',
                         'constructor_nationality', 'season_year', 'round_number']]

        # Return new DataFrame.
        return df

    except:
        return 'Unable to parse data - check URL.'


def con_standings(url):
    """
    User passes in URL that is extracted, transformed and loaded -
    Returns filename and DataFrame.
    """
    try:
        # Request and store returned data.
        r = requests.get(url)
        r.raise_for_status()

        # Get the actual data from the requested.
        data = r.json()['MRData']['StandingsTable']['StandingsLists'][0]

        # Pass the data and return it.
        return parse_con_standings(data)

    # Except for non-200 status.
    except requests.exceptions.HTTPError:
        return 'Status code not 200 - invalid URL.'
    # Unable to store in data variable.
    except KeyError:
        return "URL entered likely wasn't for Constructor Standings"


def parse_con_url(season_year, round_no):
    """Function to turn user selection into URL to query API."""
    return f'https://ergast.com/api/f1/{season_year}/{round_no}/constructorStandings.json'


def search_con_db(year, round):
    """
    Function to search the passed in database to return the matching rows in a DF.
    """
    # Connect to the database.
    db = get_db()

    # Find the matching data.
    data_match = db.execute(
        'SELECT * FROM constructor_standings'
        ' WHERE season_year = ? AND round_number = ?',
        (year, round)
    ).fetchall()

    # Convert to a DataFrame.
    df = pd.DataFrame(data_match,
                        columns=["UID",
                                 "Position",
                                 "Constructor Name",
                                 "Points",
                                 "Wins",
                                 "Constructor Url",
                                 "Constructor Nationality",
                                 "Season Year",
                                 "Round Number"]).set_index("UID")

    # Return the DataFrame.
    return df
