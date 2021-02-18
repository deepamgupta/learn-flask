# __init__.py file tells python that the folder it is in is a package
# this initializes and ties everything required to run the project

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '78e88e5bd9a75d2122e757aa130020be' # Provides a protection from hackers
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # for the login_required decorator in which is applies in routes.py. Here 'login' is the name of the function, not the url
login_manager.login_message_category = 'info' # for making the message look good

from flaskblog import routes

