"""INIT"""
import os
from datetime import datetime 
#mainuplates dates/times
from flask import Flask
#web framwork
from authlib.integrations.flask_client import OAuth
#create registry with OAuth
from dotenv import load_dotenv
#reads .env file
from flask_wtf.csrf import CSRFProtect
#to use secrete key 
from .extensions import db, login_manager
#import extensions file
load_dotenv()
#load variables from .env
app = Flask(__name__)
#set flask app
csrf = CSRFProtect(app)
#
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)
#allows users 
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#datetime formatting, modify behavior of function
@app.template_filter()
def datetimeformat(value, format='%Y-%m-%d'):
    """datetimeformat"""
    try:
        timestamp = int(value)
        return datetime.utcfromtimestamp(timestamp).strftime(format)
    except ValueError:
        return value  
#Auth0 python code
oauth = OAuth(app)
#the follow information was given in Auth0 website
oauth.register(
    "auth0",
    client_id=os.environ.get("AUTH0_CLIENT_ID"),
    client_secret=os.environ.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{os.environ.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# import models and routes after initializing extensions
from .models import User  
from . import routes
@login_manager.user_loader
def load_user(user_id):
    """load user"""
    return User.query.get(int(user_id))
