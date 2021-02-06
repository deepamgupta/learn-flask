from flask import Flask, render_template, url_for
app = Flask(__name__)


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

if __name__ == "__main__":
    app.run(debug=True)