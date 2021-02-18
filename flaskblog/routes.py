from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Post
from flaskblog.form import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.password = hashed_password
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created, you are now able to log in!", "success")
        return redirect(url_for('login')) # url_for(arg), here arg is function name, not route name.
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check email and password.", "danger")
    return render_template('login.html', title="Login", form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required # look for login_manager.login_view in __init__.py . Try to access this page without logging in and it will redirect to the login page and add a "next" parameter in the url
def account():
    return render_template('account.html', title="Account")

