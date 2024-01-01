# Gabriela Pedreros - gp21j
""" This file defines database models using SQLAlchemy. Flask-Login is used for
    user management """
from flask_login import UserMixin        #used in user model to check if user is authenticated
from flaskblog import db                #import database to work on it 

class NewsItem(db.Model):        #create NewItem model, which will hold the hackernews post information
    """ NewsItems class contains all News Item data """
    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String(100))
    descendants = db.Column(db.Integer)
    kids = db.Column(db.String(300))    # Assume 'kids' is a string representing a list
    score = db.Column(db.Integer)
    text = db.Column(db.Text)
    time = db.Column(db.Integer)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))
    url = db.Column(db.String(200))
    def __repr__(self):
        return f"NewsItem('{self.title}', '{self.url}')"

class User(db.Model, UserMixin):    #create User model which will hold all information about a user
    """ User class contains all user data """
    id = db.Column(db.Integer, primary_key=True)
    auth0_user_id = db.Column(db.String(120), unique=True, nullable=False)  # Auth0 User ID
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=True)        #setting all users to be an admin
    def __repr__(self):
        """Important user data returned"""
        return f"User('{self.username}', '{self.email}')"

class NewsItemLike(db.Model):    #NewItemLike model to see the relationship between a user and the post
    """ NewsItemLike class contains all user/post interaction data """
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
