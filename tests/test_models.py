# test_models.py
import pytest
from flaskblog import app, db
from flaskblog.models import NewsItem, User, NewsItemLike

@pytest.fixture(scope='module')
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def test_db(test_app):
    # This fixture ensures a clean state for each test function
    yield db

def test_user_creation(test_db):
    user = User(username='testuser', email='test@example.com', auth0_user_id='auth0|testuser')
    test_db.session.add(user)
    test_db.session.commit()
    assert User.query.filter_by(username='testuser').first() is not None

def test_news_item_creation(test_db):
    news_item = NewsItem(title='Test News', url='http://example.com', by='author')
    test_db.session.add(news_item)
    test_db.session.commit()
    assert NewsItem.query.filter_by(title='Test News').first() is not None

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
