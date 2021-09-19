from blog import app
from flask import render_template
from blog.models import Post


@app.route('/')
def homepage():
    # i post sono ordinati per data di creazione decrescente  
    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("homepage.html", posts=posts)

@app.route('/about')
def about_page():
    return render_template("about_page.html")

