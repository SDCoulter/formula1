""" Test connection to the database and its initialization. """

import sqlite3, pytest
from formula1_data.db import get_db


def test_get_close_db(app):
    # Test connection to the test database and connection is made.
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # Try to execute a search on the database while unconnected.
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    # Assert that we couldn't make the search because the connection is closed.
    assert 'closed' in str(e.value)


# Test initialization process of db.
def test_init_db_command(runner, monkeypatch):
    # Create object to record the initialization.
    class Recorder(object):
        called = False

    # Fake function to change the status of the Recorder class.
    def fake_init_db():
        Recorder.called = True

    # Instead of running init_db, confirm it was called by running fake_init_db.
    monkeypatch.setattr('formula1_data.db.init_db', fake_init_db)
    # Run the argument on the command line.
    result = runner.invoke(args=['init-db'])
    # Output will match if db initialized with no issue.
    assert 'Database Initialized.' in result.output
    # Check function was called.
    assert Recorder.called
