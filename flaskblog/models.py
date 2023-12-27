"""Models imports and libraries"""
from flask_login import UserMixin
#check if user is authenticated
from flaskblog import db
#import database to work on it 
#create NewItem model, which will hold the hackernews post information
class NewsItem(db.Model):
    """NewsItems come from HackerNewsPortal"""
    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String(100))
    descendants = db.Column(db.Integer)
    # Assume 'kids' is a string representing a list
    kids = db.Column(db.String(300))
    score = db.Column(db.Integer)
    text = db.Column(db.Text)
    time = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    url = db.Column(db.String(200))
    def __repr__(self):
        return f"NewsItem('{self.title}', '{self.url}')"
#create User model which will hold all information about a user
class User(db.Model, UserMixin):
    """User class contains all user data"""
    id = db.Column(db.Integer, primary_key=True)
    auth0_user_id = db.Column(db.String(120), unique=True, nullable=False)  # Auth0 User ID
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
#setting all users to be an admin
    is_admin = db.Column(db.Boolean, default=True)
    def __repr__(self):
        """Important user data returned"""
        return f"User('{self.username}', '{self.email}')"
#NewItemLike model to see the relationship between a user and the post
class NewsItemLike(db.Model):
    """Who likes posts"""
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    user = db.relationship('User', backref='likes')
    news_item_id = db.Column(db.Integer, db.ForeignKey('news_item.id'), primary_key=True)
    like = db.Column(db.Boolean)  
#true=like, false=dislike
    def __repr__(self):
        return (
            f"<NewsItemLike user_id='{self.user_id}' "
            f"news_item_id='{self.news_item_id}' like='{self.like}'>"
        )
