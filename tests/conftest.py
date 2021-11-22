"""
Test file for the formula1_data application.
"""

import os, tempfile, pytest
from formula1_data import create_app
from formula1_data.db import get_db, init_db

# Pull the data from the test SQL file.
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

# Create a test fixture.
@pytest.fixture
def app():
    # Create a temp database.
    db_fd, db_path = tempfile.mkstemp()
    # Create temp app.
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    # Create connection to the test database in the context of the test app.
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    # Return app as generator.
    yield app

    # CLose the connection after testing.
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
