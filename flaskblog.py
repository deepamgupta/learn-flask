from flask import Flask, render_template, url_for, flash, redirect
from form import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '78e88e5bd9a75d2122e757aa130020be' # Provides a protection from hackers

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