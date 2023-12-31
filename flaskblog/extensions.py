# Gabriela Pedreros - gp21j
""" Extensions for database handling and user management """
from flask_sqlalchemy import SQLAlchemy  #adds support for sqlalchemy to use with flask 
from flask_login import LoginManager    #user session mangement 
db = SQLAlchemy()                        #initialize database connection
login_manager = LoginManager()          #initialize user management 
