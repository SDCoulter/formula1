"""
Function(s) to query the database or API and return it, as well as dynamic data
to update the webpage.
"""

from . import moves


def get_con_df(db, sy, r_name, first=False):
    """ Query constructor standings db table or API if no data returned. """
    
    # Organise data to pass back to the webpage.
    pd = {'season_year': sy, 'round_no': r_name}
    # Get round number integer.
    r_num = int(r_name.split(' ')[0])

    try:
        # Query to the database for the table of values.
        df = moves.search_con_db(sy, r_num)
        # Raise an error if the table is empty.
        if len(df) == 0:
            raise

    # Make API call.
    except Exception as e:
        # If first query of database, use most current data on API.
        if first:
            df = moves.con_standings('https://ergast.com/api/f1/current/constructorStandings.json')
        else:
            df = moves.con_standings(moves.parse_con_url(sy, r_num))

        # If there was no returned error (a string value), insert into database.
        if type(df) != str:
            df.to_sql(name='constructor_standings', con=db, if_exists='append')
            # Rename the columns to be more presentable.
            df.columns = moves.pretty_con_names()

    # Return DF and pass_data.
    return df, pd
