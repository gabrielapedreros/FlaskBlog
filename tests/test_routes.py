# test_routes.py
import pytest
from flaskblog import app, db
from flaskblog.models import User

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    app.config['SECRET_KEY'] = 'my_precious_secret_key'  # Set a secret key for testing
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data  

def test_about_page(test_client):
    response = test_client.get('/about')
    assert response.status_code == 200
    assert b'About' in response.data  # Replace 'About' with actual text expected on your about page

