import pytest
from formula1_data.db import get_db


# Test the index route.
def test_index(client, app):
    response = client.get('/')
    # Check page renders as expected.
    assert b"Formula 1" in response.data
    assert b"GitHub Repo" in response.data
    assert b"Constructor Standings Analysis" in response.data

    # Check data.sql values are in database.
    with app.app_context():
        db = get_db()
        res = db.execute('SELECT COUNT(id) FROM data_exps WHERE id = 8000').fetchone()[0]
        assert res == 1


# Test con_standings.
def test_con_standings(client, app):
    response = client.get('/con_standings')
    # Check page.
    assert b"Constructor Standings" in response.data
    assert b"Constructor Name" in response.data
    assert b"2021" in response.data

    # Pass a post method to con_standings.
    response = client.post('/con_standings', data={'season_year': 2017, 'round_no': '5 - Spanish Grand Prix'})
    assert b"5" in response.data
    assert b"Spanish" in response.data
    assert b"2017" in response.data

    with app.app_context():
        db = get_db()
        # Search for the posted data in the db.
        res = db.execute('SELECT * FROM constructor_standings WHERE season_year == 2017').fetchone()
        assert res['constructor_name'] == 'Mercedes'

    # Send the client post again, so the app is forced to check the db for the new info.
    response = client.post('/con_standings', data={'season_year': 2017, 'round_no': '5 - Spanish Grand Prix'})
    assert b"5" in response.data

    # Pass a failing post and check error output.
    response = client.post('/con_standings', data={'season_year': 2022, 'round_no': '2020 - Spanish Grand Prix'})
    assert b"Status Code Error" in response.data
