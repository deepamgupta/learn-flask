import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    # html form will add the 'filename' attribute to the form_picture value automatically.
    # os.path.split will give two values viz. file_name and file_extension, but here we just want to use the extension, so in python if we donot want to use a variable, we name it as underscore('_') like we did here with filename
    picture_fn = random_hex + f_ext # picture_filename
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # resizing the images to 125 px, else large images will take much space on the file system
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def delete_picture(image_file):
    image_path = os.path.join(app.root_path, 'static/profile_pics', image_file)
    os.remove(image_path)


@app.route('/account', methods=['GET', 'POST'])
@login_required # look for login_manager.login_view in __init__.py . Try to access this page without logging in and it will redirect to the login page and add a "next" parameter in the url
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if current_user.image_file != 'default.jpg':
                delete_picture(current_user.image_file)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for('static', filename='profile_pics/' + current_user.image_file)

    # if file not present
    if not os.path.exists(image):
        image = url_for('static', filename='profile_pics/' + 'default.jpg')
    return render_template('account.html', title="Account", image_file=image, form=form)

