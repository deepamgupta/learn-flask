from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    # we will hash the image_file url to a string of length 20
    # also we will have a default profile pic for every user
    password = db.Column(db.String(60), nullable=False)
    # we will hash the password given by user to a string of length 60
    posts = db.relationship('Post', backref='author', lazy=True)

    # 'Post' is the class name
    # 'backref' creates a column named author in the post table, and using this we can get the author of a particular post using the 'author' attribute
    # 'lazy' argument defines when Sqlalchemy loads the data into the database, so True means sqlalchemy will load the data necessary in one go
    # with this relationship, we will be able to get all the post created by a single user.

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod # when the method has nothing to do with the instance of that class in which it is defined(i.e. it doesn't contains usage of 'self'), then, that method is declared as staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # in date_posted the default value, datetime.utc function is passed as a variable
    # we are not calling datetime.utcnow with parenthesis
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # here 'user.id', 'user' is the table name in db(which sqlalchemy creates by default as the lowercase of classname) and not the class name

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
