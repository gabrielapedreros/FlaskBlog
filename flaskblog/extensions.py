# Gabriela Pedreros - gp21j
"""Extensions"""
from flask_sqlalchemy import SQLAlchemy
#adds support for sqlalchemy to use with flask 
from flask_login import LoginManager
#user session mangement 
db = SQLAlchemy()
login_manager = LoginManager()
