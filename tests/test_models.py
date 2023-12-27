""" Testing model file """
import pytest
# pytest is a testing framework 
from flaskblog import app, db
# import Flask application instance 
# import database instance from Flask app
from flaskblog.models import NewsItem, User, NewsItemLike
# import the users

""" This fixture function is ran before the test functions, where test_app is set up once before the first test
 and torn down after last test, as described by scope='module' """
@pytest.fixture(scope='module')
def test_app():
    app.config['TESTING'] = True
    # set Flask app to testing mode 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # use in-memory SQLite database
    with app.app_context():    # commands used to connect to database
        db.create_all()        # create database tables defined in models
        yield app              # this fixture ensures a clean state for each test function
        db.drop_all()          # clean up database 
        
""" This fixture function is ran once before each test function, as described by scope='function'. test_db 
 depends on test_app """
@pytest.fixture(scope='function')
def test_db(test_app):
    # this fixture ensures a clean state for each test function
    yield db

""" Test function for users in database """
def test_user_creation(test_db):
    user = User(username='testuser', email='test@example.com', auth0_user_id='auth0|testuser')
    test_db.session.add(user)
    test_db.session.commit()
    assert User.query.filter_by(username='testuser').first() is not None
    # ensures that the user exists

""" Test function for news items in database """
def test_news_item_creation(test_db):
    news_item = NewsItem(title='Test News', url='http://example.com', by='author')
    test_db.session.add(news_item)
    test_db.session.commit()
    assert NewsItem.query.filter_by(title='Test News').first() is not None
    # ensures that the news item exists

""" Test function for which users like a news item in database """
def test_news_item_like_creation(test_db):
    user = User(username='liker', email='liker@example.com', auth0_user_id='auth0|liker')
    news_item = NewsItem(title='Likeable News', url='http://likable.com', by='author')
    test_db.session.add(user)
    test_db.session.add(news_item)
    test_db.session.commit()
    like = NewsItemLike(user_id=user.id, news_item_id=news_item.id, like=True)
    test_db.session.add(like)
    test_db.session.commit()
    assert NewsItemLike.query.filter_by(user_id=user.id, news_item_id=news_item.id).first().like is True
    # ensures that the like/disklike from a user on a news item exists
