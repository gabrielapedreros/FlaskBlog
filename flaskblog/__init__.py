# Gabriela Pedreros - gp21j
""" Initialize a Flask application with user authentication, CSFR protection, and database 
interactions """
import os
from datetime import datetime                          #manipulates dates/times
from flask import Flask                                #web framwork
from authlib.integrations.flask_client import OAuth    #create registry with OAuth
from dotenv import load_dotenv                         #reads .env file
from flask_wtf.csrf import CSRFProtect                 #to use secrete key 
from .extensions import db, login_manager              #for database interactions

load_dotenv()                                        #load variables from .env
app = Flask(__name__)                                #create Flask instance 
csrf = CSRFProtect(app)                            #initialize CSFR protections for flask app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)                                    #initialize database with Flask app

login_manager.init_app(app)                        #allow user interaction with Flask app
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@app.template_filter()
def datetimeformat(value, format='%Y-%m-%d'):    #datetime formatting, modify behavior of function
    """ datetimeformat formats the value parameter, the date, to the format passed in """
    try:
        timestamp = int(value)
        return datetime.utcfromtimestamp(timestamp).strftime(format)
    except ValueError:
        return value  

oauth = OAuth(app)                                #initialize OAuth with Flask app
oauth.register(                                #the follow code was given in the Auth0 website
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
    """ load user from database"""
    return User.query.get(int(user_id))
