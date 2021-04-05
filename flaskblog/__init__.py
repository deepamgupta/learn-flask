# __init__.py file tells python that the folder it is in is a package
# this initializes and ties everything required to run the project

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'  # for the login_required decorator in which is applies in routes.py. Here 'login' is the name of the function, not the url
login_manager.login_message_category = 'info'  # for making the message look good

mail = Mail()


# extension to our app: db, bcrypt, login_manager, mail


def create_app(
        config_class=Config):  # this will allow us to create multiple instances of our app with different configurations

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
