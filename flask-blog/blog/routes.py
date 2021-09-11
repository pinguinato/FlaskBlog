from blog import app
from flask import render_template

@app.route('/')
def homepage():
    posts = [
        {"title": "Primo post", "body": "Random body"}, 
        {"title": "Secondo post", "body": "More random content"} 
    ]
    some_boolean_flag = False

    return render_template("homepage.html", posts=posts, boolean_flag=some_boolean_flag)


