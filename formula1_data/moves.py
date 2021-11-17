"""
A place to store the functions to be used to call data from API.
"""

import pandas as pd
import requests

# Blank DF to return if there's an error.
BLANK_DF = pd.DataFrame()



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
        df['UID'] = df['position'].apply(lambda value: str(season_year) + p_z(round_no) + p_z(value))

        df = df.set_index('UID').drop(columns=['positionText', 'Constructor'])
        df.columns = ['Position', 'Points', 'Wins', 'Constructor Name', 'Constructor URL',
                          'Constructor Nationality', 'Season Year', 'Round Number']
        df = df[['Position', 'Constructor Name', 'Points', 'Wins', 'Constructor URL',
                         'Constructor Nationality', 'Season Year', 'Round Number']]

        # Create a name.
        name = f"{season_year}_r{p_z(round_no)}_Constructor_Standings"

        # Return filename and new DataFrame.
        return name, df

    except:
        return 'Unable to parse data - check URL.', BLANK_DF


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
        return 'Status code not 200 - invalid URL.', BLANK_DF
    # Unable to store in data variable.
    except KeyError:
        return "URL entered likely wasn't for Constructor Standings", BLANK_DF
