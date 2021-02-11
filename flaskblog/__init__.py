# __init__.py file tells python that the folder it is in is a package
# this initializes and ties everything required to run the project

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '78e88e5bd9a75d2122e757aa130020be' # Provides a protection from hackers
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


from flaskblog import routes

