# Gabriela Pedreros - gp21j
""" Testing routes file """
import pytest
# pytest is a testing framework 
from flaskblog import app, db
# import Flask application instance 
# import database instance from Flask app
from flaskblog.models import User
# import the users model

@pytest.fixture(scope='module')
def test_client():
    """ This fixture function is ran before the test functions, where test_client is set up once 
    before the first test and torn down after last test, as described by scope='module' """
    app.config['TESTING'] = True
    # set Flask app to testing mode 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # use in-memory SQLite database
    app.config['SECRET_KEY'] = 'my_precious_secret_key'  # set a secret key for testing
    with app.app_context():    # commands used to connect to database
        db.create_all()        # create database tables defined in models
        yield app.test_client() # this fixture ensures a clean state for each test function
        db.drop_all()          # clean up database 

def test_home_page(test_client):
    """ Test client request to app """
    response = test_client.get('/') #send get request to home page of Flask app
    assert response.status_code == 200    #loaded successfully
    assert b'Home' in response.data  #ensure home page exists

def test_about_page(test_client):
    """ Test client request to app """
    response = test_client.get('/about') #send get request to home page of Flask app
    assert response.status_code == 200    #loaded successfully
    assert b'About' in response.data  #ensure about page exists
