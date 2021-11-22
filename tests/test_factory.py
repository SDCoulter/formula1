# Test the factory function.
from formula1_data import create_app

def test_config():
    # Test passing test config works as it should.
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_app_func(client):
    # Test app functionality route.
    response = client.get('/app_func')
    assert response.data == b'The application is functioning.'
