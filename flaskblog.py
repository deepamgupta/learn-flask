from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from jinja2.nodes import Pos

from form import RegistrationForm, LoginForm
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '78e88e5bd9a75d2122e757aa130020be' # Provides a protection from hackers
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
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

posts = [
    {
        "author": "Deepam Gupta", 
        "title": "Blog Post 1",
        "content": "Content 1",
        "date_posted": "March 18, 2020"
    },
    {
        "author": "Bhoomika Pandey", 
        "title": "Blog Post 2",
        "content": "Content 2",
        "date_posted": "Jan 14, 2020"
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", posts=posts)

@app.route('/about')
def about():
    return render_template("about.html", title="About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for('home')) # url_for(arg), here arg is function name, not route name.
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been successfully logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check username and password.", "danger")
    return render_template('login.html', title="Login", form=form)

if __name__ == "__main__":
    app.run(debug=True)